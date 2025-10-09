import streamlit as st
from sqlalchemy import select
from src.db.engine import SessionLocal
from src.db.crud import ensure_demo_user, create_achievement, get_or_create_user
from src.services.star_service import generate_star
from src.db.models import User
import time

st.set_page_config(page_title="Log Achievement", layout="wide")
st.header("🏠 Log Achievement → Generate STAR")

# --- Initialize session state for button ---
if "star_generated" not in st.session_state:
    st.session_state.star_generated = False

# --- Load existing usernames ---
with SessionLocal() as s:
    existing_users = s.scalars(select(User.display_name)).all()
existing_users.sort()

username_option = st.selectbox(
    "Select Existing User or Add New", 
    options=["➕ Add New User"] + existing_users
)

# --- If new, show input ---
if username_option == "➕ Add New User":
    new_username = st.text_input("New Username", value="")
    active_username = new_username.strip()
else:
    active_username = username_option


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

redirect_placeholder = st.empty()

# Action: Save achievement & generate STAR story
if st.button("Save & Generate STAR", disabled=st.session_state.star_generated):
    if not raw.strip():
        st.warning("Please enter an achievement.")
    else:
        with st.spinner("Generating STAR story..."):
            with SessionLocal() as s:
                user = get_or_create_user(s, active_username, role)
                ach = create_achievement(s, user.id, role, raw.strip())
                story = generate_star(s, user.id, ach.id, role, raw.strip())
                s.commit()

                st.success(f"✅ User `{user.display_name}` saved. STAR story created.")
                st.text_area("Generated STAR Story", value=story.full_text or "", height=220)

        st.session_state.star_generated = True
    
        with redirect_placeholder.container():
            with st.spinner("Redirecting to STAR Stories..."):
                time.sleep(5) 
        st.switch_page("pages/02_🧩_STAR_Stories.py")
