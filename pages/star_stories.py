import streamlit as st
from sqlalchemy import select, desc
from src.db.engine import SessionLocal
from src.db.models import StarStory, InterviewQuestion
from src.services.question_service import generate_questions

st.set_page_config(page_title="STAR Stories", layout="wide")
st.header("🧩 STAR Stories & Questions")

with SessionLocal() as s:
    stories = list(s.execute(
        select(StarStory).order_by(desc(StarStory.created_at)).limit(25)
    ).scalars())

if not stories:
    st.info("No STAR stories yet. Go to 'Log Achievement' to create one.")
else:
    for story in stories:
        with st.expander(f"STAR for Achievement #{story.achievement_id} — {story.created_at}"):
            cols = st.columns(4)
            cols[0].markdown("**Situation**"); cols[0].write(story.situation or "")
            cols[1].markdown("**Task**"); cols[1].write(story.task or "")
            cols[2].markdown("**Action**"); cols[2].write(story.action or "")
            cols[3].markdown("**Result**"); cols[3].write(story.result or "")

            st.markdown("**Full Story**")
            st.write(story.full_text or "")

            if st.button("Generate 6 Questions", key=f"gen_q_{story.id}"):
                with SessionLocal() as s2:
                    qs = generate_questions(
                        s2, user_id=1,
                        achievement_id=story.achievement_id,
                        star_text=story.full_text or "",
                        n=6
                    )
                    s2.commit()
                    st.success(f"✅ {len(qs)} questions saved.")

            # List existing questions
            with SessionLocal() as s3:
                qs = list(s3.execute(
                    select(InterviewQuestion)
                    .where(InterviewQuestion.achievement_id == story.achievement_id)
                    .order_by(desc(InterviewQuestion.created_at))
                ).scalars())

            if qs:
                st.markdown("**Generated Questions**")
                for q in qs:
                    st.write(f"- {q.question_text}")
