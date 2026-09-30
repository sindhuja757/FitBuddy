# FitBuddy: AI Fitness Plan Generator

Generates personalized 3-day workout plans with Gemini.

## Run
1. python -m venv venv
2. venv\Scripts\activate
3. python -m pip install -r requirements.txt
4. Create .env with GOOGLE_API_KEY=AIzaSy...
5. python -m uvicorn app.main:app --reload
6. Open http://127.0.0.1:8000