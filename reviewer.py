import json
import os
import requests


def review(content:dict,grade: int) -> dict:
    system_prompt = (
        """You are an educational quality reviewer. 
        Evaluate content strictly for the specified grade level.
        Respond ONLY with a valid JSON object — no markdown, no explanation, no backticks.""")

    user_prompt = f"""Review this Grade {grade} educational content:

{json.dumps(content, indent=2)}
Check for:
1. Age/grade appropriateness of language and concepts
2. Conceptual correctness
3. Clarity of explanation
4. MCQ quality (each question tests only what was taught in the explanation)


Return exactly this JSON structure:
{{
  "status": "pass",
  "feedback": []
}}

feedback should be an array of specific, actionable issues if any are found.
 If no issues are found, return an empty array and set status to "pass".
Set status to "fail" and populate feedback with specific actionable issues if any are found.
Example feedback: "Sentence 2 uses the word 'perpendicular' which is too advanced for Grade {grade}"."""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + os.getenv("MISC_API_KEY"),
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            "temperature": 0.3,
        },
        timeout=30,
    )
    response.raise_for_status()

    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)

    with open("reviewer_output.json", "w") as f:
        json.dump(result, f, indent=2)

    return result