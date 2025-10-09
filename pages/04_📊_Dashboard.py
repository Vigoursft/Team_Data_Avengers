import streamlit as st
import pandas as pd
from sqlalchemy import text
from src.db.engine import engine, SessionLocal
from src.db.crud import dashboard_stats

st.set_page_config(page_title="Dashboard", layout="wide")
st.header("📊 Dashboard")

# KPIs
with SessionLocal() as s:
    stats = dashboard_stats(s)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Achievements", stats["achievements"])
c2.metric("STAR Stories", stats["stories"])
c3.metric("Questions", stats["questions"])
c4.metric("Answers", stats["answers"])
c5.metric("Total Tokens", stats["tokens"])

# Token trend
@st.cache_data(ttl=30)
def load_tokens():
    with engine.begin() as conn:
        return pd.read_sql(text("""
            SELECT date_trunc('day', created_at) AS day,
                   feature,
                   SUM(total_tokens) AS tokens
            FROM token_usage
            GROUP BY 1,2
            ORDER BY 1
        """), conn)

df = load_tokens()
st.subheader("Token usage over time")
if df is not None and not df.empty:
    st.bar_chart(df, x="day", y="tokens", color="feature")
else:
    st.info("No token usage data yet.")
