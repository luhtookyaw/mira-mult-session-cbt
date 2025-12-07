# narrativize_storyline.py
import json
import os
from datetime import datetime
from typing import Dict, Any

from event_narratizer import narrativize_period


PERIOD_KEYS = [
    "before_session_1",
    "between_sessions_1_2",
    "between_sessions_2_3",
    "between_sessions_3_4",
    "between_sessions_4_5",
    "between_sessions_5_6",
    "between_sessions_6_7",
    "between_sessions_7_8",
    "between_sessions_8_9",
]


def load_storyline(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def narrativize_storyline(storyline: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes a storyline dict and returns a dict of diary paragraphs
    keyed by the same period keys.

    Each entry looks like:
    {
      "timeframe": ...,
      "summary": ...,
      "diary_paragraph": ...
    }
    """
    diary: Dict[str, Any] = {}
    previous_paragraph = None

    for key in PERIOD_KEYS:
        if key not in storyline:
            # Skip missing keys gracefully
            continue

        period_data = storyline[key]
        events = period_data.get("events", [])

        paragraph = narrativize_period(events, previous_paragraph=previous_paragraph)

        diary[key] = {
            "timeframe": period_data.get("timeframe", ""),
            "summary": period_data.get("summary", ""),
            "diary_paragraph": paragraph,
        }

        previous_paragraph = paragraph

    return diary


def save_diary(diary: Dict[str, Any], original_path: str) -> str:
    """
    Save the diary JSON next to the storyline, or in a separate folder.
    """
    base_dir = os.path.dirname(os.path.abspath(original_path))
    out_dir = os.path.join(base_dir, "output_diaries")
    os.makedirs(out_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(original_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = f"{base_name}_diary_{timestamp}.json"
    out_path = os.path.join(out_dir, out_name)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(diary, f, ensure_ascii=False, indent=2)

    return out_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Narrativize a stored storyline JSON into diary-style paragraphs."
    )
    parser.add_argument(
        "storyline_path",
        type=str,
        help="Path to the storyline JSON file (e.g., output_storylines/storyline_20250207_162355.json)",
    )

    args = parser.parse_args()
    storyline_path = args.storyline_path

    print(f"Loading storyline from: {storyline_path}")
    storyline = load_storyline(storyline_path)

    print("Narrativizing periods...")
    diary = narrativize_storyline(storyline)

    out_path = save_diary(diary, storyline_path)
    print(f"Diary saved to: {out_path}")
