# helpers.py (or put at bottom of llm.py)
import json
from typing import Any
from llm import call_llm

def call_llm_json(
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-4o-mini",
) -> Any:
    """
    Call LLM and parse strict JSON response.
    Assumes the model really outputs only JSON.
    """
    raw = call_llm(system_prompt, user_prompt, model=model)
    raw = raw.strip()
    # optional: try to trim if the model accidentally wraps text
    if raw.startswith("```"):
        raw = raw.strip("`")
        # remove optional "json" language tag
        raw = raw.replace("json", "", 1).strip()
    return json.loads(raw)

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()