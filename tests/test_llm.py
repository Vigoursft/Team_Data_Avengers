from src.ai.llm import chat_json

def test_chat_json_parses(mock_llm_json):
    payload = mock_llm_json({"hello":"world"})
    data, usage, model = chat_json([{"role":"user","content":"x"}], model="gpt-4o-mini")
    assert data == payload
    assert usage.prompt_tokens >= 0 and usage.completion_tokens >= 0

