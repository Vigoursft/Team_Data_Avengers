from sqlalchemy.orm import Session
from src.db.crud import log_tokens
from src.db.models import InterviewAnswer, Feedback
from src.ai.llm import chat_json
from src.ai.prompts import FEEDBACK_SYS, FEEDBACK_USER

def generate_feedback(session: Session, user_id: int, role: str, question_id: int, question: str, answer: str):
    data, usage, model = chat_json([
        {"role": "system", "content": FEEDBACK_SYS},
        {"role": "user", "content": FEEDBACK_USER.format(role=role, question=question, answer=answer)}
    ])

    # Store answer
    answer_obj = InterviewAnswer(
        user_id=user_id,
        question_id=question_id,
        answer_text=answer.strip()
    )
    session.add(answer_obj)
    session.flush()  # ensure answer_obj.id is assigned

    # Prepare feedback data
    rubric = data.get("rubric", {})
    summary = data.get("summary", "")
    suggestions = data.get("suggestions", [])
    suggestions_text = "\n".join(suggestions) if isinstance(suggestions, list) else str(suggestions)

    # Store feedback
    feedback_obj = Feedback(
        user_id=user_id,
        answer_id=answer_obj.id,
        rubric=rubric,
        summary=summary,
        suggestions=suggestions_text,
        tokens_input=getattr(usage, "prompt_tokens", 0),
        tokens_output=getattr(usage, "completion_tokens", 0),
        model_used=model
    )
    session.add(feedback_obj)

    log_tokens(
        session,
        user_id,
        "FEEDBACK",
        model,
        getattr(usage, "prompt_tokens", 0),
        getattr(usage, "completion_tokens", 0)
    )
    return data
