# tests/test_services_questions.py
import pytest
from unittest.mock import MagicMock
from src.services.question_service import generate_questions

@pytest.fixture
def session_mock():
    # Create a mock SQLAlchemy session
    session = MagicMock()
    return session

def test_generate_questions_returns_list(session_mock):
    user_id = 1
    achievement_id = 42
    star_text = "Successfully completed task X"
    
    # Patch the bulk_insert_questions and log_tokens functions inside the service
    from src.services import question_service
    question_service.bulk_insert_questions = MagicMock()
    question_service.log_tokens = MagicMock()
    
    # Patch chat_json to return predictable output
    question_service.chat_json = MagicMock(return_value=(
        ["Question 1?", "Question 2?", "Question 3?"],  # data
        MagicMock(prompt_tokens=10, completion_tokens=20),  # usage
        "gpt-test-model"  # model
    ))
    
    # Call the function
    questions = generate_questions(session_mock, user_id, achievement_id, star_text, n=3)
    
    # Assertions
    assert isinstance(questions, list)
    assert len(questions) == 3
    assert questions == ["Question 1?", "Question 2?", "Question 3?"]
    
    # Check that database mocks were called
    question_service.bulk_insert_questions.assert_called_once_with(session_mock, user_id, achievement_id, questions)
    question_service.log_tokens.assert_called_once()
