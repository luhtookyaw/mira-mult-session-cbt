# event_narratizer.py
from typing import Dict, Any, List, Optional
import json
import os

from llm import call_llm
from helpers import load_prompt  # your existing helper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NARR_SYS_PATH = os.path.join(BASE_DIR, "prompts", "event_narratizer_system.txt")


def narrativize_period(
    events: List[Dict[str, Any]],
    previous_paragraph: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Turn a list of JSON events for a given period into ONE diary-style paragraph.

    - events: list of event dicts following your EVENT SCHEMA
    - previous_paragraph: last diary paragraph, or None if this is the first entry
    - returns: a single paragraph (string)
    """

    if not events:
        # Defensive: no events -> empty string or a very short neutral paragraph
        return ""

    system_prompt = load_prompt(NARR_SYS_PATH)

    events_json = json.dumps(events, ensure_ascii=False, indent=2)

    if previous_paragraph:
        prev_text = previous_paragraph.strip()
    else:
        prev_text = ""

    user_prompt_parts = []

    if prev_text:
        user_prompt_parts.append(
            "PREVIOUS DIARY PARAGRAPH (IMMEDIATELY BEFORE THIS PERIOD):\n"
            f"{prev_text}\n"
        )
    else:
        user_prompt_parts.append(
            "NO previous diary paragraph is available for this client. "
            "Write a stand-alone diary paragraph for this period.\n"
        )

    user_prompt_parts.append(
        "CURRENT PERIOD EVENTS (JSON LIST):\n"
        f"{events_json}\n\n"
        "TASK:\n"
        "- Based ONLY on these events, write ONE new diary-style paragraph.\n"
        "- Respect all factual and stylistic constraints from the system prompt.\n"
        "- Do NOT invent new major events; stay within the JSON.\n"
        "- Aim for ~150–300 words, one paragraph."
    )

    user_prompt = "\n".join(user_prompt_parts)

    narrative = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
    )

    # Ensure it's a single paragraph (strip extra newlines if any)
    narrative = " ".join(narrative.splitlines()).strip()
    return narrative