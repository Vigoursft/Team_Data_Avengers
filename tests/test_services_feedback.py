import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, InterviewAnswer, Feedback
from src.services.feedback_service import generate_feedback

# ---------------------------
# Fixture: in-memory DB session
# ---------------------------
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")  # temporary in-memory DB
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


# ---------------------------
# Test: generate_feedback
# ---------------------------
def test_generate_feedback(db_session):
    user_id = 1
    role = "engineer"
    question_id = 101
    question = "Explain a challenging bug you fixed"
    answer = "I identified a memory leak and optimized the code"

    # Call the function
    feedback_data = generate_feedback(
        session=db_session,
        user_id=user_id,
        role=role,
        question_id=question_id,
        question=question,
        answer=answer
    )

    # ---------------------------
    # Assertions
    # ---------------------------
    # Check returned data
    assert "rubric" in feedback_data
    assert "summary" in feedback_data
    assert "suggestions" in feedback_data

    # Check DB entries
    answer_in_db = db_session.query(InterviewAnswer).filter_by(user_id=user_id).first()
    assert answer_in_db is not None
    assert answer_in_db.answer_text == answer.strip()

    feedback_in_db = db_session.query(Feedback).filter_by(user_id=user_id).first()
    assert feedback_in_db is not None
    assert feedback_in_db.answer_id == answer_in_db.id
    assert isinstance(feedback_in_db.rubric, dict)
    assert isinstance(feedback_in_db.suggestions, str)
