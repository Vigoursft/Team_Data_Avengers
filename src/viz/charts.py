import streamlit as st
import pandas as pd

def token_bar(df: pd.DataFrame):
    if not df.empty:
        st.bar_chart(df, x="day", y="tokens", color="feature")