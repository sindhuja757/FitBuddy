import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-3.8-flash"


async def generate_nutrition_tip(goal):
    prompt = f"Give one short nutrition tip for someone with goal: {goal}."
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"API Error: {str(e)}"