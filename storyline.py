# storyline.py
from typing import Dict, Any, List
import json
import os

from helpers import call_llm_json
from helpers import load_prompt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "storyline_system.txt")

def generate_global_storyline(
    intake_text: str,
    patterns: List[str],
    core_thought: str,
) -> Dict[str, Any]:
    """
    Generic storyline generator for ANY CACTUS client.
    The only case-specific inputs are:
      - intake_text
      - patterns
      - core_thought
    The prompts themselves are reusable.
    """

    system_prompt = load_prompt(PROMPT_PATH)

    user_prompt = f"""
INTAKE FORM (RAW TEXT):
{intake_text}

COGNITIVE DISTORTION PATTERNS (LIST):
{json.dumps(patterns, ensure_ascii=False)}

CORE AUTOMATIC THOUGHT (TEXT):
"{core_thought}"

INSTRUCTIONS:
- Read the intake and infer:
  - The main recurring situations where distress occurs.
  - The central fears, beliefs, and emotions.
  - The main life domains that matter to this client (e.g., work, family, study, friends, daily life).
- Use this inferred information to decide:
  - Which events are DIRECT TRIGGERS of the presenting difficulty.
  - Which events are PARALLEL TRIGGERS in other domains.
  - Which events are BARRIERS (other stressors interfering with change).
  - Which events are BACKGROUND (ordinary life events that give context).
- Follow the EVENT SCHEMA and JSON output format defined in the system prompt.
- Do NOT mention therapy, counseling, or sessions. Only describe life events.
"""

    return call_llm_json(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )
