import os
from google import genai

MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.8-flash")

def update_workout(original_plan, feedback, goal):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return original_plan + f"\n\nUSER FEEDBACK RECEIVED:\n{feedback}\n\nDemo mode: connect GEMINI_API_KEY to regenerate the plan with Gemini."

    client = genai.Client(api_key=key)
    prompt = f"""
You are updating a general fitness plan.
Goal: {goal}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Return a revised 7-day plan that incorporates reasonable feedback.
Keep it safe, general, and practical. Do not provide medical diagnosis or
treatment. Preserve useful parts of the original plan unless feedback requires
a change.
"""
    return client.models.generate_content(model=MODEL, contents=prompt).text
