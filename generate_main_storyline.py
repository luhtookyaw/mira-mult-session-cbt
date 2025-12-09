# main_storyline_test.py
import json
import os
from datetime import datetime
from storyline import generate_global_storyline

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
    "black-and-white or polarized thinking / all or nothing thinking"
]

CORE_THOUGHT = "I frequent this animal shelter. All of the animals remembered me except a few, I can never go back there again they will hate me."

if __name__ == "__main__":
    storyline = generate_global_storyline(INTAKE, PATTERNS, CORE_THOUGHT)

    # Pretty print to console (optional)
    import pprint
    pprint.pp(storyline)

    # === SAVE TO FILE ===
    
    # Create output directory (safe even if exists)
    os.makedirs("output_storylines", exist_ok=True)

    # Create a timestamp-based filename for reproducibility
    filename = f"storyline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = os.path.join("output_storylines", filename)

    # Save JSON
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(storyline, f, ensure_ascii=False, indent=2)

    print(f"\nStoryline saved to: {filepath}")
