import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-3.8-flash"


async def stream_workout_gemini(goal, intensity):
    prompt = f"""You are a professional fitness trainer. Create a personalized 3-day workout plan.
Fitness goal: {goal}
Intensity: {intensity}
For each day include: Warm-up, Main Workout (sets/reps), Cooldown.
Format: Day 1: ... Day 2: ... Day 3: ...
Keep it concise and clear."""
    try:
        stream = client.models.generate_content_stream(model=MODEL_NAME, contents=prompt)
        for chunk in stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"API Error: {str(e)}"


async def update_workout_plan(original, feedback):
    prompt = f"""Original 3-day plan:\n{original}\n\nUser feedback: "{feedback}"\nRevise the plan keeping the same format."""
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"API Error: {str(e)}"