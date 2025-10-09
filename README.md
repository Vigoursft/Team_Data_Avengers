# AI-Powered Interview & Career Growth Tool  
Serverless Stack: **Streamlit + PostgreSQL + OpenAI**

Turns raw work achievements into **STAR stories**, generates **role-specific mock questions**, collects **AI feedback**, and tracks **token usage** – all in one Streamlit app.

---

### Quick Start
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # fill your OPENAI_API_KEY & DATABASE_URL

# Initialize database:
psql "$DATABASE_URL" -f scripts/init_db.sql

streamlit run app.py
