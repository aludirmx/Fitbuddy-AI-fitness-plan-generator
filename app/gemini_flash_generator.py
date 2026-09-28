import os
from google import genai

MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-3.8-flash")

def generate_tip(goal):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return fallback_tip(goal)

    client = genai.Client(api_key=key)
    prompt = f"""
Give one concise, practical general nutrition or recovery tip for a fitness
user whose goal is {goal}. Avoid medical claims, extreme dieting, or unsafe
recommendations. Keep it under 80 words.
"""
    return client.models.generate_content(model=MODEL, contents=prompt).text

def fallback_tip(goal):
    tips = {
        "Weight loss": "Focus on regular balanced meals, adequate hydration, sleep, and sustainable activity rather than extreme restriction.",
        "Muscle gain": "Include regular protein-containing foods and enough overall food to support training and recovery.",
        "General wellness": "Stay hydrated, eat a varied balanced diet, sleep consistently, and include regular enjoyable movement."
    }
    return tips.get(goal, tips["General wellness"])
