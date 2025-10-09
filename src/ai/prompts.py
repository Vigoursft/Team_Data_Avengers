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

Score 1–5: clarity, technical_depth, structure, impact, relevance.
Return STRICT JSON:
{
  "rubric": {"clarity":int,"technical_depth":int,"structure":int,"impact":int,"relevance":int},
  "summary": "...",
  "suggestions": ["...","...","..."]
}
ONLY JSON.
"""
