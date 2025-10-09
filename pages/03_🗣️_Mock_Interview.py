import streamlit as st
from sqlalchemy import select, desc
from src.db.engine import SessionLocal
from src.db.models import InterviewQuestion, User
from src.services.feedback_service import generate_feedback

st.set_page_config(page_title="Mock Interview", layout="wide")
st.header("🗣️ Mock Interview & Feedback")

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
    questions = s.execute(
        select(InterviewQuestion)
        .where(InterviewQuestion.user_id == selected_user.id)
        .order_by(desc(InterviewQuestion.created_at))
        .limit(50)
    ).scalars().all()

if not questions:
    st.info("No questions yet for this user. Generate them from a STAR story first.")
else:
    # Step 4: Pick question
    q_map = {f"Q#{q.id}: {q.question_text[:80]}": q for q in questions}
    choice = st.selectbox("Pick a question", list(q_map.keys()))
    # role = st.selectbox(
    #     "Role",
    #     ["Backend Engineer", "Frontend Engineer", "Data Engineer", "DevOps / SRE"]
    # )
    answer = st.text_area("Your answer (1–2 paragraphs)", height=200)

    if st.button("Get Feedback"):
        qobj = q_map[choice]
        with SessionLocal() as s2:
            fb = generate_feedback(
                s2,
                user_id=selected_user.id,
                role=role,
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
