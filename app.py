import streamlit as st

st.set_page_config(page_title="AI Career Coach", page_icon="🤖", layout="wide")
st.title("AI-Powered Interview & Career Growth Tool")

st.page_link("pages/01_🏠_Log_Achievement.py", label="Log Achievement & Generate STAR")
st.page_link("pages/02_🧩_STAR_Stories.py", label="STAR Stories & Questions")
st.page_link("pages/03_🗣️_Mock_Interview.py", label="Mock Interview & Feedback")
st.page_link("pages/04_📊_Dashboard.py", label="Dashboard")
st.page_link("pages/05_👤_Profile.py", label="Profile")