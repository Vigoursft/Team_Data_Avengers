import streamlit as st
from src.db.engine import SessionLocal
from src.db.crud import ensure_demo_user, create_achievement
from src.services.star_service import generate_star

st.set_page_config(page_title="Log Achievement", layout="wide")
st.header("🏠 Log Achievement → Generate STAR")

# Select role and write achievement
role = st.selectbox(
    "Role",
    ["Backend Engineer", "Frontend Engineer", "Data Engineer", "DevOps / SRE"]
)
raw = st.text_area(
    "Achievement (1–3 lines)",
    placeholder="e.g., Reduced API latency by 45% by adding Redis caching and fixing N+1 queries.",
    height=140
)

# Action: Save achievement & generate STAR story
if st.button("Save & Generate STAR"):
    if not raw.strip():
        st.warning("Please enter an achievement.")
    else:
        with SessionLocal() as s:
            user = ensure_demo_user(s)
            ach = create_achievement(s, user.id, role, raw.strip())
            story = generate_star(s, user.id, ach.id, role, raw.strip())
            s.commit()

            st.success("✅ STAR story created and saved")
            st.text_area("Generated STAR Story", value=story.full_text or "", height=220)
