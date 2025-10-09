import json, re
from openai import OpenAI
from src.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def _clean(t: str) -> str:
    t = t.strip()
    t = re.sub(r"^```(?:json)?\\n", "", t)
    t = re.sub(r"```$", "", t)
    return t

def chat_json(messages, model=None, temperature=0.2):
    model = model or settings.MODEL_FAST
    resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
    usage = resp.usage
    text = _clean(resp.choices[0].message.content or "")
    try:
        data = json.loads(text)
    except Exception:
        b, e = text.find("{"), text.rfind("}")
        data = json.loads(text[b:e+1]) if b!=-1 and e!=-1 else {"_raw": text}
    return data, usage, model
