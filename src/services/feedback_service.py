from sqlalchemy.orm import Session
from src.db.crud import log_tokens
from src.ai.llm import chat_json
from src.ai.prompts import FEEDBACK_SYS, FEEDBACK_USER

def generate_feedback(session: Session, user_id: int, role: str, question: str, answer: str):
    data, usage, model = chat_json([
        {"role":"system","content":FEEDBACK_SYS},
        {"role":"user","content":FEEDBACK_USER.format(role=role, question=question, answer=answer)}
    ])
    log_tokens(session, user_id, "FEEDBACK", model,
               getattr(usage,"prompt_tokens",0), getattr(usage,"completion_tokens",0))
    return data
