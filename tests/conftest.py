# Shared fixtures: in-memory DB, session, and LLM mocks
import types
import json
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your app modules
from src.db.models import Base
from src.db import engine as app_engine_mod
from src.db.engine import SessionLocal as AppSessionLocal
from src.ai import llm as llm_mod
from src.config import settings

@pytest.fixture(scope="session")
def test_engine():
    # Fast, isolated DB for unit tests
    # eng = create_engine("sqlite+pysqlite:///:memory:", future=True)
    eng = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
    Base.metadata.create_all(eng)
    return eng

@pytest.fixture(scope="function")
def db_session(test_engine, monkeypatch):
    # Override app engine/session with test engine
    TestSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False, future=True)
    monkeypatch.setattr(app_engine_mod, "engine", test_engine, raising=False)
    monkeypatch.setattr("src.db.engine.SessionLocal", TestSession, raising=False)

    s = TestSession()
    try:
        yield s
    finally:
        s.close()

class _Usage:  # small helper to mimic OpenAI usage object
    def __init__(self, p=42, c=101, t=None):
        self.prompt_tokens = p
        self.completion_tokens = c
        self.total_tokens = t if t is not None else p + c

class _ChoiceMsg:
    def __init__(self, content):
        self.message = types.SimpleNamespace(content=content)

class _Choices:
    def __init__(self, content):
        self.choices = [_ChoiceMsg(content)]
        self.usage = _Usage()

class FakeChatCompletions:
    def __init__(self, canned_json):
        self._canned = canned_json

    def create(self, model, messages, temperature=0.0):
        # Return strict JSON text, wrapped or not
        return types.SimpleNamespace(
            choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=self._canned))],
            usage=_Usage()
        )

class FakeOpenAI:
    def __init__(self, canned_json):
        self.chat = types.SimpleNamespace(completions=FakeChatCompletions(canned_json))

@pytest.fixture
def mock_llm_json(monkeypatch):
    """Monkeypatch src.ai.llm.client to return canned JSON content."""
    def _apply(payload_dict):
        canned = json.dumps(payload_dict)
        fake = FakeOpenAI(canned_json=canned)
        monkeypatch.setattr(llm_mod, "client", fake, raising=True)
        # lock model for determinism
        monkeypatch.setattr(settings, "MODEL_FAST", "gpt-4o-mini", raising=False)
        return payload_dict
    return _apply
