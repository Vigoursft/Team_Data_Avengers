from sqlalchemy import select
from src.services.star_service import generate_star
from src.db.crud import get_or_create_user, create_achievement
from src.db.models import StarStory, TokenUsage

def test_generate_star_saves_story_and_tokens(db_session, mock_llm_json):
    # clear previous token usage
    db_session.query(TokenUsage).delete()
    db_session.commit()

    mock_llm_json({
        "situation":"S", "task":"T", "action":"A", "result":"R",
        "full_text":"S T A R."
    })
    user = get_or_create_user(db_session, "Taylor-test", "Backend")
    ach = create_achievement(db_session, user.id, "Backend Engineer", "Implemented caching to reduce latency.")
    story = generate_star(db_session, user.id, ach.id, "Backend Engineer", "Implemented caching to reduce latency.")
    db_session.commit()

    stored = db_session.get(StarStory, story.id)
    assert stored and stored.full_text.startswith("S")

    # token usage logged
    total = db_session.execute(select(TokenUsage)).scalars().all()
    assert len(total) == 1 and total[0].feature == "STAR"
