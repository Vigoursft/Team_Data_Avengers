import streamlit as st
from sidebar import render_sidebar

st.set_page_config(page_title="AI Career Coach", page_icon="favicon-32x32-1.png", layout="wide")

# Call sidebar render function
render_sidebar()

st.title("AI-Powered Interview & Career Growth Tool")

st.page_link("pages/01_🏠_Log_Achievement.py", label="Log Achievement & Generate STAR")
st.page_link("pages/02_🧩_STAR_Stories.py", label="STAR Stories & Questions")
st.page_link("pages/03_🗣️_Mock_Interview.py", label="Mock Interview & Feedback")
st.page_link("pages/04_📊_Dashboard.py", label="Dashboard")
st.page_link("pages/05_📘_Mock_QA_Archive.py", label="Mock Q&A Archive")
st.page_link("pages/06_👤_Profile.py", label="Profile")