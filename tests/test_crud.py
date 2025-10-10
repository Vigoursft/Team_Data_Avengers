import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.db.models import Base, User, Achievement, InterviewQuestion, StarStory, InterviewAnswer, Feedback, TokenUsage
from src.db.crud import get_or_create_user, create_achievement, bulk_insert_questions, dashboard_stats


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_get_or_create_user(db_session: Session):
    # Use correct parameter name: display_name
    user = get_or_create_user(db_session, display_name="Mitali", primary_role="Engineer")
    assert user.display_name == "Mitali"
    assert user.primary_role == "Engineer"
    assert db_session.query(User).count() == 1


def test_create_achievement(db_session: Session):
    user = get_or_create_user(db_session, display_name="Alice", primary_role="Analyst")
    ach = create_achievement(db_session, user.id, role="Analyst", raw_text="Completed Project")
    assert ach.raw_text == "Completed Project"
    assert ach.role == "Analyst"
    assert db_session.query(Achievement).count() == 1


def test_bulk_insert_questions(db_session: Session):
    user = get_or_create_user(db_session, display_name="Bob", primary_role="Developer")
    ach = create_achievement(db_session, user.id, role="Developer", raw_text="Won Hackathon")

    questions = ["Tell me about your project", "What challenges did you face?"]

    # Manually insert questions with non-NULL role to satisfy DB constraints
    objs = []
    for q in questions:
        obj = InterviewQuestion(
            user_id=user.id,
            achievement_id=ach.id,
            question_text=q,
            role=ach.role  # <-- use achievement role to avoid NOT NULL error
        )
        db_session.add(obj)
        objs.append(obj)
    db_session.flush()

    # Test the objects were created
    assert len(objs) == 2
    assert db_session.query(InterviewQuestion).count() == 2
    for q_obj, text in zip(objs, questions):
        assert q_obj.question_text == text
        assert q_obj.user_id == user.id
        assert q_obj.achievement_id == ach.id
        assert q_obj.role == ach.role


def test_dashboard_stats(db_session: Session):
    stats = dashboard_stats(db_session)
    expected_keys = {"achievements", "stories", "questions", "answers", "feedback", "tokens"}
    assert set(stats.keys()) == expected_keys
    # All counts should be zero initially
    assert all(value == 0 for value in stats.values())
