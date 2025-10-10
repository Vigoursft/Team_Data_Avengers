import streamlit as st
from sqlalchemy import select, desc
from src.db.engine import SessionLocal
from src.db.models import User, InterviewQuestion, InterviewAnswer, Feedback
from sidebar import render_sidebar
import json

st.set_page_config(page_title="📘 Mock Q&A Archive", layout="wide")
st.title("📘 Mock Q&A Archive")
st.caption("Browse all user's interview questions, answers, and feedback.")


with SessionLocal() as session:
    users = session.execute(select(User).order_by(User.display_name)).scalars().all()

    render_sidebar()

    if not users:
        st.warning("No users found.")
    else:
        for user in users:
            st.subheader(f"👤 {user.display_name}")

            # Fetch that user's questions
            questions = session.execute(
                select(InterviewQuestion)
                .where(InterviewQuestion.user_id == user.id)
                .order_by(desc(InterviewQuestion.created_at))
            ).scalars().all()

            if not questions:
                st.caption("No questions yet.")
                continue

            for i, q  in enumerate(questions, start=1):
                with st.expander(f" {i} . {q.question_text}", expanded=False):
                    # Fetch answer
                    answer = session.execute(
                        select(InterviewAnswer)
                        .where(InterviewAnswer.question_id == q.id)
                        .order_by(desc(InterviewAnswer.created_at))
                    ).scalars().first()

                    if answer:
                        st.markdown("**📝 Answer**")
                        st.write(answer.answer_text)

                        # Fetch feedback
                        feedback = session.execute(
                            select(Feedback)
                            .where(Feedback.answer_id == answer.id)
                            .order_by(desc(Feedback.created_at))
                        ).scalars().first()

                        if feedback:
                            st.markdown("**🧾 Feedback**")
                            st.write("🔍 Rubric:")
                            st.json(feedback.rubric or {})

                            st.markdown("**🧠 Summary**")
                            st.write(feedback.summary or "")

                            st.markdown("**💡 Suggestions**")
                            suggestions = []
                            try:
                                suggestions = json.loads(feedback.suggestions)
                            except Exception:
                                # fallback if not JSON, treat as single string
                                suggestions = [feedback.suggestions] if feedback.suggestions else []

                            for suggestion in suggestions:
                                st.write(f"- {suggestion}")
                        else:
                            st.warning("⚠️ No feedback yet.")
                    else:
                        st.warning("⚠️ No answer provided.")
