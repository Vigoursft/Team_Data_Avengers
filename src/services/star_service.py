from sqlalchemy.orm import Session
from src.db.models import StarStory
from src.db.crud import log_tokens
from src.ai.llm import chat_json
from src.ai.prompts import STAR_SYS, STAR_USER

def generate_star(session: Session, user_id: int, achievement_id: int, role: str, raw: str):
    data, usage, model = chat_json([
        {"role":"system","content":STAR_SYS},
        {"role":"user","content":STAR_USER.format(role=role, raw=raw)}
    ])
    story = StarStory(
        user_id=user_id, achievement_id=achievement_id,
        situation=data.get("situation",""), task=data.get("task",""),
        action=data.get("action",""), result=data.get("result",""),
        full_text=data.get("full_text",""),
        tokens_input=getattr(usage,"prompt_tokens",0),
        tokens_output=getattr(usage,"completion_tokens",0),
        model_used=model
    )
    session.add(story)
    log_tokens(session, user_id, "STAR", model,
               getattr(usage,"prompt_tokens",0), getattr(usage,"completion_tokens",0))
    return story
