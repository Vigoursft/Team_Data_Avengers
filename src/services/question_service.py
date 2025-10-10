from sqlalchemy.orm import Session
from src.db.crud import bulk_insert_questions, log_tokens
from src.ai.llm import chat_json
from src.ai.prompts import QUEST_SYS, QUEST_USER
import json
import re

def generate_questions(session: Session, user_id: int, achievement_id: int, star_text: str, n=3):
    data, usage, model = chat_json([
        {"role": "system", "content": QUEST_SYS},
        {"role": "user", "content": QUEST_USER.format(n=n, star=star_text)}
    ], temperature=0.3)

    # Try to extract from _raw if needed
    if not isinstance(data, list):
        raw = data.get("_raw", "")
        raw = re.sub(r"^```(?:json)?\n", "", raw.strip())
        raw = re.sub(r"\n```$", "", raw)
        try:
            data = json.loads(raw)
        except Exception:
            data = []

    qs = [q.strip() for q in data if isinstance(q, str)]
    bulk_insert_questions(session, user_id, achievement_id, qs)

    log_tokens(session, user_id, "QUESTIONS", model,
               getattr(usage, "prompt_tokens", 0),
               getattr(usage, "completion_tokens", 0))

    return qs
