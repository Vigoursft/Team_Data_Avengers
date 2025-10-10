import streamlit as st
from sqlalchemy import select, desc
from src.db.engine import SessionLocal
from src.db.models import StarStory, InterviewQuestion, User
from src.services.question_service import generate_questions
from sidebar import render_sidebar

st.set_page_config(page_title="STAR Stories", page_icon="favicon-32x32-1.png", layout="wide")
st.header("🧩 STAR Stories & Questions")

# Read session state (safe defaults)
last_user_id = st.session_state.get("last_user_id")
last_star_id = st.session_state.get("last_star_id")
# Call sidebar render function
render_sidebar()

with SessionLocal() as s:
    q = select(StarStory).order_by(desc(StarStory.created_at)).limit(50)
    stories = list(s.execute(q).scalars())

    if not stories:
        st.info("No STAR stories yet. Go to 'Log Achievement' to create one.")
    else:
        if last_star_id:
            st.success("Jumped to your latest STAR story 👇")
        for story in stories:
            expanded = (story.id == last_star_id)  # auto-open the latest one

            user = s.execute(select(User).where(User.id == story.user_id)).scalar_one_or_none()
            user_display_name = user.display_name if user else "Unknown User"

            formatted_time = story.created_at.strftime("%b %d, %Y %I:%M %p %Z")
            with st.expander(f"#{user_display_name} STAR for Achievement on — {formatted_time}",expanded=expanded):
                cols = st.columns(4)
                cols[0].markdown("**Situation**"); cols[0].write(story.situation or "")
                cols[1].markdown("**Task**"); cols[1].write(story.task or "")
                cols[2].markdown("**Action**"); cols[2].write(story.action or "")
                cols[3].markdown("**Result**"); cols[3].write(story.result or "")

                st.markdown("**Full Story**")
                st.write(story.full_text or "")

                if st.button("Generate 3 Questions", key=f"gen_q_{story.id}"):
                    qs = generate_questions(
                        s,
                        user_id=story.user_id,
                        achievement_id=story.achievement_id,
                        star_text=story.full_text or "",
                        n=3
                    )
                    s.commit()
                    st.success(f"✅ {len(qs)} questions generated.")

                # List existing questions
                qs = list(s.execute(
                    select(InterviewQuestion)
                    .where(InterviewQuestion.achievement_id == story.achievement_id)
                    .order_by(desc(InterviewQuestion.created_at))
                ).scalars())

                if qs:
                    st.markdown("**Generated Questions**")
                    for q in qs:
                        st.write(f"- {q.question_text}")
