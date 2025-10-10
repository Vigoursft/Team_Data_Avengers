import streamlit as st
from sidebar import render_sidebar

st.set_page_config(page_title="Profile", page_icon="favicon-32x32-1.png", layout="wide")
st.header("👤 Profile")

# Call sidebar render function
render_sidebar()

# This can be replaced with actual user info once authentication is added
st.write("**Name:** Admin User")
st.write("**Primary Role:** DevOps / SRE")
st.write("**Joined:** Thursday, October 9, 2025 (demo)")

st.caption("In a production system, this page would show editable user profile data and activity summary.")
