import os
from google import genai

MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.8-flash")

def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)

def generate_workout(name, age, weight, goal, intensity):
    prompt = f"""
Create a safe, general 7-day fitness plan for a user named {name}.
Age: {age}
Weight: {weight} kg
Goal: {goal}
Workout intensity: {intensity}

Return a clear day-by-day plan. For each day include:
1. Warm-up
2. Main workout with exercises and sets/reps or duration
3. Cooldown/recovery

Include rest/recovery where appropriate. Do not diagnose medical conditions,
prescribe treatment, or encourage unsafe exercise. Keep the response practical
and beginner-friendly. Add a short note that the plan is general information
and the user should stop if they experience pain or feel unwell.
"""
    client = _client()
    if not client:
        return demo_plan(goal, intensity)

    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

def demo_plan(goal, intensity):
    return f"""7-DAY SAMPLE PLAN
Goal: {goal}
Intensity: {intensity}

Day 1 – Full Body
Warm-up: 5–10 minutes easy movement
Main: Bodyweight squats 3x10, wall/incline push-ups 3x8, glute bridges 3x12
Cooldown: 5 minutes gentle stretching

Day 2 – Cardio
Warm-up: 5 minutes
Main: 20 minutes comfortable walking/cycling intervals
Cooldown: 5 minutes

Day 3 – Recovery
Easy walking and gentle mobility for 15–20 minutes.

Day 4 – Lower Body
Warm-up: 5–10 minutes
Main: Squats 3x10, reverse lunges 2x8 each side, calf raises 3x12
Cooldown: 5 minutes

Day 5 – Upper Body
Warm-up: 5–10 minutes
Main: Incline push-ups 3x8, resistance-band rows 3x10, shoulder mobility
Cooldown: 5 minutes

Day 6 – Light Cardio + Core
Main: 20 minutes easy cardio plus dead bug 2x8 each side and bird-dog 2x8.

Day 7 – Rest
Recovery, hydration, sleep, and gentle mobility.

This is a demonstration plan, not medical advice. Stop if you feel pain or unwell.
"""
