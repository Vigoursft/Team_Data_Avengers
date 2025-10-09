import streamlit as st
st.set_page_config(page_title="AI Interview Coach", layout="wide")
st.title("AI-Powered Interview & Career Growth Tool")

st.page_link("pages/log_achievement.py", label="Log Achievement & Generate STAR")
st.page_link("pages/star_stories.py", label="STAR Stories & Questions")
st.page_link("pages/mock_interview.py", label="Mock Interview & Feedback")
st.page_link("pages/dashboard.py", label="Dashboard")
st.page_link("pages/profile.py", label="Profile")
