import streamlit as st

st.set_page_config(page_title="Profile", layout="wide")
st.header("👤 Profile")

# This can be replaced with actual user info once authentication is added
st.write("**Name:** Demo User")
st.write("**Primary Role:** Backend Engineer")
st.write("**Joined:** Today (demo)")

st.caption("In a production system, this page would show editable user profile data and activity summary.")
