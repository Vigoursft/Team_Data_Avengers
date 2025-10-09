from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    template: str


SYSTEM_PROMPT = PromptTemplate(
    name="system_default",
    template="You are a helpful AI assistant.",
)


TEMPLATES: Dict[str, PromptTemplate] = {
    SYSTEM_PROMPT.name: SYSTEM_PROMPT,
}


def get_prompt(name: str) -> PromptTemplate:
    """Return a prompt template by name or raise a clear error."""
    if name in TEMPLATES:
        return TEMPLATES[name]
    raise KeyError(f"Unknown prompt template: {name}")


