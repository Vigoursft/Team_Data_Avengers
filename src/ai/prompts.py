ACH_VALIDATOR_SYS = "Classify if the text is a concrete work achievement suitable for STAR."

ACH_VALIDATOR_USER = """You are validating whether the following text is a concrete work achievement suitable for STAR interview prep.

Text:
{raw}

If it is vague, extremely short, or clearly placeholder (e.g., "test", "abc"), mark valid=false.

Return STRICT JSON in this exact format:
{{{{"valid": true|false, "reason": "short reason", "missing": ["action","impact","scope"]}}}}
No explanations or markdown.
"""


STAR_SYS = "You are a career coach who writes concise, interview-ready STAR stories for software engineers."

STAR_USER = """Role: {role}
Achievement (raw): {raw}

Write a STAR story (Situation, Task, Action, Result), 150–220 words, concise and measurable.
Return STRICT JSON: situation, task, action, result, full_text. ONLY JSON.
"""

QUEST_SYS = "You are an experienced interviewer for this role."

QUEST_USER = """Based on this STAR story, generate {n} interview questions (mix behavioral & technical).
STAR:
{star}
Return ONLY a JSON list of strings.
"""

FEEDBACK_SYS = "You are a strict but helpful interviewer giving structured feedback."

FEEDBACK_USER = """Role: {role}
Question: {question}
Candidate answer: {answer}

Instructions:
- Evaluate the candidate's answer strictly based on what is written. Do not assume missing details.
- If the answer is weak (e.g., "test result", vague, or unrelated), reflect that honestly in the feedback.
- Score the answer in 3 areas from 1 to 5:
  - clarity
  - technical_depth
  - structure
  - impact
  - relevance

- Provide:
  - A rubric with the 3 scores.
  - A short summary (1–2 lines) of strengths and weaknesses.
  - 2–3 helpful improvement suggestions.

Return ONLY valid JSON in this exact format:

{{
  "rubric": {{
    "clarity": int,
    "technical_depth": int,
    "structure": int,
    "impact": int,
    "relevance": int
  }},
  "summary": "Your summary here.",
  "suggestions": [
    "First suggestion.",
    "Second suggestion.",
    "Third suggestion."
  ]
}}

No markdown, no explanations — just clean JSON.
"""
