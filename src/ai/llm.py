from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ModelConfig:
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: Optional[int] = None


class LLMClient:
    """Simple LLM client interface to be wired to a provider later."""

    def __init__(self, config: Optional[ModelConfig] = None) -> None:
        self.config = config or ModelConfig()

    def generate(self, messages: List[ChatMessage]) -> str:
        """Generate a response for a chat conversation.

        This is a placeholder implementation. Replace with real provider logic.
        """
        return "LLM response placeholder"


