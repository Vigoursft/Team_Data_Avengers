import streamlit as st
from sqlalchemy import select, desc
from src.db.engine import SessionLocal
from src.db.models import InterviewQuestion, User, InterviewAnswer
from src.services.feedback_service import generate_feedback
from sidebar import render_sidebar

st.set_page_config(page_title="Mock Interview", page_icon="favicon-32x32-1.png", layout="wide")
st.header("🗣️ Mock Interview & Feedback")

# Call sidebar render function
render_sidebar()

with SessionLocal() as s:
    # Step 1: Load distinct users
    users = s.execute(select(User).order_by(User.display_name)).scalars().all()

if not users:
    st.warning("No users found.")
    st.stop()

# Step 2: Select user from dropdown
user_map = {user.display_name: user for user in users}
selected_user_name = st.selectbox("Select User", list(user_map.keys()))
selected_user = user_map[selected_user_name]

# Step 3: Load questions for selected user
with SessionLocal() as s:
    answered_qs = select(InterviewAnswer.question_id)
    questions = s.execute(
        select(InterviewQuestion)
        .where(InterviewQuestion.user_id == selected_user.id)
        .where(InterviewQuestion.id.not_in(answered_qs))
        .order_by(desc(InterviewQuestion.created_at))
        .limit(50)
    ).scalars().all()

if not questions:
    st.info("No questions yet for this user. Generate them from a STAR story first.")
else:
    # Step 4: Pick question
    q_map = {f"{i+1}. {q.question_text[:250]}": q for i, q in enumerate(questions)}
    choice = st.selectbox("Pick a question", list(q_map.keys()))

    answer = st.text_area("Your answer (1–2 paragraphs)", height=200)

    if st.button("Get Feedback"):
        qobj = q_map[choice]
        with SessionLocal() as s2:
            fb = generate_feedback(
                s2,
                user_id=selected_user.id,
                role=selected_user.primary_role,
                question_id=qobj.id,
                question=qobj.question_text,
                answer=answer.strip()
            )
            s2.commit()

        st.success("✅ Feedback generated")

        rub = fb.get("rubric", {})
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Clarity", rub.get("clarity", "-"))
        c2.metric("Tech Depth", rub.get("technical_depth", "-"))
        c3.metric("Structure", rub.get("structure", "-"))
        c4.metric("Impact", rub.get("impact", "-"))
        c5.metric("Relevance", rub.get("relevance", "-"))

        st.markdown("**Summary**")
        st.write(fb.get("summary", ""))

        st.markdown("**Suggestions**")
        for tip in fb.get("suggestions", []):
            st.write(f"- {tip}")
