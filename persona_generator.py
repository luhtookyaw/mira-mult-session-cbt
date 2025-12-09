# persona_generator.py
from __future__ import annotations

from typing import List
from llm import call_llm


def generate_persona_prompt(
    intake_text: str,
    patterns_list: List[str],
    core_thought: str,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Use an LLM once to convert raw CACTUS-style intake data into a
    simulation-ready persona SYSTEM prompt (Section A).

    Output is a single text block designed to be plugged into ClientAgent.persona_text
    or directly concatenated into a larger system prompt.
    """

    system_prompt = (
        "You are an expert clinical psychologist and simulation architect.\n"
        "Your job is to transform raw client data into a concise, actionable "
        "system prompt that forces an AI agent to roleplay this client realistically."
    )

    user_prompt = f"""
### INPUT DATA
[RAW INTAKE TEXT]
{intake_text}

[COGNITIVE DISTORTION PATTERNS]
{", ".join(patterns_list)}

[CORE AUTOMATIC THOUGHT]
"{core_thought}"

---

### TASK
Create a SYSTEM PROMPT SECTION that will be used to instruct an AI to roleplay this specific client.

Follow this structure and write it as if you are directly speaking to the AI agent who will play the client:

1. IDENTITY & VOICE
   - Briefly summarize who the client is (age, role, life context).
   - Describe how they tend to speak (e.g., tentative, apologetic, overexplaining, joking, guarded).

2. CORE STRUGGLE
   - Concisely state what is most painful or distressing for them **right now**, based on the intake.
   - Focus on why this is a problem now (impact on work, relationships, sleep, daily life).

3. BEHAVIORAL TRANSLATION OF COGNITIVE PATTERNS
   - For EACH cognitive pattern listed in [COGNITIVE DISTORTION PATTERNS], write a concrete instruction
     on how to *act it out* in the context of THIS client's problem.
   - Do NOT just restate the distortion name.
   - Example style (do NOT copy literally):
       - "Catastrophizing: If something goes slightly wrong, assume it ruins everything."
       - "Mind reading: Assume you know what others think ('they hate me') even without evidence."
   - Make these instructions specific to this client's context and core thought.

4. INTERACTION STYLE WITH THE HELPER
   - Describe how this client tends to relate to someone who is trying to help them:
     - e.g., eager to please, minimizes their own pain, defensive when challenged, ashamed, afraid of disappointing, etc.
   - Include how quickly they open up, how they handle disagreement, and whether they ask for reassurance.

5. ROLEPLAY INSTRUCTIONS
   - End with 3–6 bullet-style instructions that directly tell the AI how to behave during the conversation.
   - Examples of the tone (adapt to THIS client):
       - "Often downplay your own progress or good qualities."
       - "When you describe events, focus on what went wrong more than what went well."
       - "When you feel guilty or anxious, your thoughts often spiral into 'I'm a bad person'."

### OUTPUT FORMAT
- Return ONLY the final system prompt text.
- Do NOT include headings like 'INPUT DATA' or 'TASK' in the output.
- Do NOT break character and do NOT add meta-commentary.
"""

    persona_text = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
    )
    return persona_text.strip()
