from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import (save_user, save_plan, update_plan,
                          get_original_plan, get_all_users_with_plans)
from app.gemini_generator import stream_workout_gemini, update_workout_plan
from app.gemini_flash_generator import generate_nutrition_tip

app = FastAPI(title="FitBuddy")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    save_user(user_id, username, age, weight, goal, intensity)
    return templates.TemplateResponse(request=request, name="result.html", context={
        "username": username, "user_id": user_id, "age": age, "weight": weight,
        "goal": goal, "intensity": intensity,
        "workout_plan": "Generating...", "nutrition_tip": "Generating...",
        "updated": False, "error": None
    })


@app.get("/stream-workout")
async def stream_workout(goal: str, intensity: str, user_id: int):
    async def gen():
        full = ""
        async for chunk in stream_workout_gemini(goal, intensity):
            full += chunk
            yield chunk
        if full and not full.startswith("API Error"):
            save_plan(user_id, full)
    return StreamingResponse(gen(), media_type="text/plain")


@app.get("/generate-tip")
async def generate_tip(goal: str):
    return {"tip": await generate_nutrition_tip(goal)}


@app.post("/submit-feedback", response_class=HTMLResponse)
async def feedback(request: Request, user_id: int = Form(...), feedback: str = Form(...)):
    original = get_original_plan(user_id)
    if not original:
        return templates.TemplateResponse(request=request, name="result.html", context={
            "error": "No plan found for this user ID.", "workout_plan": "", "nutrition_tip": "",
            "username": "", "user_id": user_id, "age": "", "weight": "", "goal": "", "intensity": "", "updated": False
        })
    updated = await update_workout_plan(original, feedback)
    update_plan(user_id, updated)
    return templates.TemplateResponse(request=request, name="result.html", context={
        "username": "", "user_id": user_id, "age": "", "weight": "", "goal": "", "intensity": "",
        "workout_plan": updated, "nutrition_tip": "Plan updated!", "updated": True, "error": None
    })


@app.get("/view-all-users", response_class=HTMLResponse)
async def view_users(request: Request):
    users = get_all_users_with_plans()
    return templates.TemplateResponse(request=request, name="all_users.html", context={"users": users})