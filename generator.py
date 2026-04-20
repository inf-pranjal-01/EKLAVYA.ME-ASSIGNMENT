


from email import header
import json
import os

import requests

from dotenv import load_dotenv
load_dotenv()

def generate( input_data : dict, feedback : list = None, prev_response : dict = None) -> dict:
    
    grade= input_data["grade"]
    topic = input_data["topic"]

    feedback_str = ""

    if feedback is not None and len(feedback) > 0:
         header = "\n\nPrevious review flagged these issues — fix them:\n"
         bullets = "\n".join(f"- {f}" for f in feedback)
         feedback_str = header + bullets


    system_prompt = f"""You are an educational content creator for Grade {grade} students. 
        Generate content that is age-appropriate, conceptually correct, and clear. 
        Respond ONLY with a valid JSON object — no markdown, no explanation, no backticks."""

    user_prompt = f"""Create educational content for Grade {grade} on the topic: "{topic}".
                     your last response was: {prev_response}.

                    
                    {feedback_str}

                    ABOSULUTEY FIX THE ISSUES AND GENERATE THE CONTENT AGAIN.
                    Return exactly this JSON structure:


                    {{
                    "explanation": "This {topic} could be understood as......",
                    "mcqs": [
                        {{
                        "question": "...",
                        "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                        "answer": "A"
                        }}
                    ]
                    }}

Include 2 MCQs. The answer field should be just the letter (A/B/C/D)."""

    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
    "Authorization": "Bearer " + os.getenv("MISC_API_KEY"),  
    },
    json = {
    "model": "openai/gpt-5.2",
    "messages": [
      {
        "role": "user",
        "content": user_prompt
      },

      {"role": "system",
       "content" : system_prompt
      },
    ],
            "temperature": 0.7,
        },

        timeout=30,
    )




    raw = response.json()["choices"][0]["message"]["content"].strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    result = json.loads(raw)

    with open("generator_output.json", "w") as f:
        json.dump(result, f, indent=2)
    
    return result
 
   
