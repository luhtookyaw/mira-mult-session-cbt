# demo_client_two_turns.py

from __future__ import annotations

import json
from pathlib import Path

from persona_generator import generate_persona_prompt
from client_agent import ClientAgent


# -----------------------------
# 1. Raw input data for persona
# -----------------------------
INTAKE = """
Name:
Brooke Davis
Age:
41
Gender:
female
Occupation: Veterinary Assistant
Education: Certified Veterinary Technician
Marital Status: Single
Family Details: Lives alone with multiple pets

2. Presenting Problem
I feel anxious and avoid going back to the animal shelter because I believe the animals there will hate me for not remembering me. This leads to feelings of guilt and self-blame.
These feelings started a few months ago after a visit to the shelter where some animals did not greet me as warmly as before.
I believe the stress level when this problem started was moderate, as I tend to internalize situations related to animals.
The problem has escalated over time, causing me to avoid the shelter altogether. The fear of being rejected by the animals has grown stronger.
I experience these negative thoughts and emotions whenever I think about returning to the animal shelter.
I have tried to challenge these thoughts on my own but have been unsuccessful in changing my beliefs.

3. Reason for Seeking Counseling
I decided to seek counseling because this issue has started affecting my daily life and my passion for working with animals.

4. Past History (including medical history)
I have not experienced similar problems before.
I have not received treatment or counseling for psychological problems in the past.
I do not have any significant physical illnesses.

5. Academic/occupational functioning level: My job performance as a veterinary assistant has not been affected yet, but my passion for working with animals has dwindled.
Interpersonal relationships: My relationships with other animal shelter volunteers have been strained as I have distanced myself because of this issue.
Daily life: My anxiety about going to the shelter has disrupted my sleep patterns and overall well-being.

6. Social Support System
I have a few close friends who are supportive, but they do not fully understand the extent of my anxiety related to the animal shelter.
"""

PATTERNS = [
    "catastrophizing",
    "discounting the positive",
    "labeling and mislabeling",
    "mental filtering",
    "jumping to conclusions: mind reading",
    "jumping to conclusions: fortune-telling",
    "personalization",
    "black-and-white or polarized thinking / all or nothing thinking",
]

CORE_THOUGHT = (
    "I frequent this animal shelter. All of the animals remembered me except a few, "
    "I can never go back there again they will hate me."
)


# -----------------------------
# 2. Helper: load storyline JSON
# -----------------------------
def load_storyline(path: str) -> dict:
    """Load an already generated storyline JSON from disk."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Storyline file not found: {path}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# 3. Demo: two client turns
# -----------------------------
def main():
    STORYLINE_PATH = "output_storylines/storyline_20251210_031731.json"

    # 1) Load storyline generated earlier
    storyline = load_storyline(STORYLINE_PATH)
    print(f"Loaded storyline from: {STORYLINE_PATH}")

    # 2) Generate persona system section from intake + patterns + core thought
    print("Generating persona system prompt from intake...")
    persona_text = generate_persona_prompt(
        intake_text=INTAKE,
        patterns_list=PATTERNS,
        core_thought=CORE_THOUGHT,
        model="gpt-4o-mini",
    )

    # 3) Initialize ClientAgent with persona
    client = ClientAgent(
        persona_text=persona_text,
        long_term_summary="",  # no prior sessions yet
        client_label="Brooke",
        model="gpt-4o-mini",
    )

    # 4) Prepare conversation history
    history = []

    # -------------------------
    # TURN 1
    # -------------------------
    therapist_line_1 = (
        "Thank you for coming today, Brooke. What has been weighing on you the most lately?"
    )

    client_reply_1 = client.generate_reply_for_session_start(
        session_index=1,
        storyline=storyline,
        therapist_utterance=therapist_line_1,
        conversation_history=history,
    )

    # Save turn 1
    history.append({"speaker": "therapist", "text": therapist_line_1})
    history.append({"speaker": "client", "text": client_reply_1})

    # -------------------------
    # TURN 2 (NEW)
    # -------------------------
    therapist_line_2 = (
        "I appreciate you sharing that. Can you tell me about a recent moment when those feelings were especially strong?"
    )

    client_reply_2 = client.generate_reply_for_session_start(
        session_index=1,
        storyline=storyline,
        therapist_utterance=therapist_line_2,
        conversation_history=history,
    )

    # Save turn 2
    history.append({"speaker": "therapist", "text": therapist_line_2})
    history.append({"speaker": "client", "text": client_reply_2})

    # -------------------------
    # PRINT RESULTS
    # -------------------------
    print("\n=== TWO-TURN DEMO ===")
    print(f"THERAPIST (Turn 1): {therapist_line_1}")
    print(f"CLIENT    (Turn 1): {client_reply_1}\n")

    print(f"THERAPIST (Turn 2): {therapist_line_2}")
    print(f"CLIENT    (Turn 2): {client_reply_2}\n")


if __name__ == "__main__":
    main()
