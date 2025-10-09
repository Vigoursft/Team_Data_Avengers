from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session
from .models import User, Achievement, StarStory, InterviewQuestion, InterviewAnswer, Feedback, TokenUsage

def ensure_demo_user(session: Session) -> User:
    user = session.scalar(select(User).limit(1))
    if not user:
        user = User(display_name="Demo User", primary_role="Backend")
        session.add(user); session.flush()
    return user

def create_achievement(session: Session, user_id: int, role: str, raw_text: str) -> Achievement:
    ach = Achievement(user_id=user_id, role=role, raw_text=raw_text)
    session.add(ach); session.flush()
    return ach

def bulk_insert_questions(session: Session, user_id: int, achievement_id: int, qs: list[str]):
    for q in qs:
        session.add(InterviewQuestion(user_id=user_id, achievement_id=achievement_id, question_text=q))

def log_tokens(session: Session, user_id: int, feature: str, model: str, p: int, c: int):
    session.add(TokenUsage(user_id=user_id, feature=feature, model_used=model,
                           prompt_tokens=p, completion_tokens=c, total_tokens=p+c))

def dashboard_stats(session: Session):
    counts = lambda table: session.scalar(select(func.count()).select_from(table)) or 0
    tokens = session.scalar(select(func.coalesce(func.sum(TokenUsage.total_tokens),0))) or 0
    return dict(
        achievements=counts(Achievement),
        stories=counts(StarStory),
        questions=counts(InterviewQuestion),
        answers=counts(InterviewAnswer),
        feedback=counts(Feedback),
        tokens=int(tokens)
    )

def get_or_create_user(session: Session, display_name: str, primary_role: str | None = None) -> User:
    """
    Fetch a user by display_name (case-insensitive). If not found, create one.
    Optionally set/refresh primary_role if provided.
    """
    display_name = (display_name or "").strip()
    if not display_name:
        display_name = "Demo User"

    user = session.scalar(
        select(User).where(func.lower(User.display_name) == display_name.lower()).limit(1)
    )
    if not user:
        user = User(display_name=display_name, primary_role=primary_role)
        session.add(user)
        session.flush()
    else:
        # Update role if provided and different
        if primary_role and user.primary_role != primary_role:
            user.primary_role = primary_role
            session.flush()
    return user

