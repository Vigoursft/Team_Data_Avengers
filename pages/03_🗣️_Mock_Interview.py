import streamlit as st
from sqlalchemy import select, desc
from src.db.engine import SessionLocal
from src.db.models import InterviewQuestion, User, InterviewAnswer
from src.services.feedback_service import generate_feedback
from sidebar import render_sidebar

st.set_page_config(page_title="Mock Interview", page_icon="favicon-32x32-1.png", layout="wide")
st.header("🗣️ Mock Interview & Feedback")

render_sidebar()

with SessionLocal() as s:
    users = s.execute(select(User).order_by(User.display_name)).scalars().all()

if not users:
    st.warning("No users found.")
    st.stop()

user_map = {user.display_name: user for user in users}
selected_user_name = st.selectbox("Select User", list(user_map.keys()))
selected_user = user_map[selected_user_name]

# Step 1: Get unanswered questions for selected user
with SessionLocal() as s:
    answered_q_ids = s.execute(
        select(InterviewAnswer.question_id).where(InterviewAnswer.user_id == selected_user.id)
    ).scalars().all()
    questions = s.execute(
        select(InterviewQuestion)
        .where(InterviewQuestion.user_id == selected_user.id)
        #.where(~InterviewQuestion.id.in_(answered_q_ids))  # only unanswered
        .order_by(desc(InterviewQuestion.created_at))
    ).scalars().all()

# Step 2: Initialize session state
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False
if "feedback" not in st.session_state:
    st.session_state.feedback = None

if not questions:
    st.info("No unanswered questions. Generate them from a STAR story first.")
else:
    total_questions = len(questions)
    current = st.session_state.current_q_index

    if current >= total_questions:
        st.success("🎉 You've answered all available questions.")
    else:
        q = questions[current]

        # Progress bar and label
        st.progress((current + 1) / total_questions)
        st.caption(f"Question {current + 1} of {total_questions}")

        st.markdown(f"**Question:** {q.question_text}")

        answer_key = f"answer_{q.id}"
        user_answer = st.text_area("Your Answer", key=answer_key, height=200)

        if not st.session_state.feedback_given:
            if st.button("Get Feedback"):
                if not user_answer.strip():
                    st.warning("Please enter your answer before submitting.")
                else:
                    with SessionLocal() as s2:
                        fb = generate_feedback(
                            s2,
                            user_id=selected_user.id,
                            role=selected_user.primary_role,
                            question_id=q.id,
                            question=q.question_text,
                            answer=user_answer.strip()
                        )
                        s2.commit()

                    st.session_state.feedback = fb
                    st.session_state.feedback_given = True

        if st.session_state.feedback_given:
            fb = st.session_state.feedback
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

            if st.button("➡️ Next Question"):
                st.session_state.current_q_index += 1
                st.session_state.feedback_given = False
                st.session_state.feedback = None
                st.rerun()
