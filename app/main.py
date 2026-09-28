from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, UserPlan
from .gemini_generator import generate_workout
from .gemini_flash_generator import generate_tip
from .updated_plan import update_workout

DATABASE_URL = "sqlite:///./fitbuddy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

@app.get("/health")
def health():
    return {"status": "ok"}
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
def generate(request: Request, name: str = Form(...), age: int = Form(...),
             weight: float = Form(...), goal: str = Form(...),
             intensity: str = Form(...)):
    plan = generate_workout(name, age, weight, goal, intensity)
    tip = generate_tip(goal)

    db = SessionLocal()
    record = UserPlan(name=name, age=age, weight=weight, goal=goal,
                      intensity=intensity, workout_plan=plan, nutrition_tip=tip)
    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    return templates.TemplateResponse("result.html", {
        "request": request, "record": record, "updated": False
    })

@app.post("/update/{plan_id}", response_class=HTMLResponse)
def update_plan(request: Request, plan_id: int, feedback: str = Form(...)):
    db = SessionLocal()
    record = db.get(UserPlan, plan_id)
    if not record:
        db.close()
        return RedirectResponse("/", status_code=303)

    new_plan = update_workout(record.workout_plan, feedback, record.goal)
    record.workout_plan = new_plan
    record.feedback = feedback
    db.commit()
    db.refresh(record)
    db.close()

    return templates.TemplateResponse("result.html", {
        "request": request, "record": record, "updated": True
    })

@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    db = SessionLocal()
    records = db.query(UserPlan).order_by(UserPlan.created_at.desc()).all()
    db.close()
    return templates.TemplateResponse("all_users.html", {
        "request": request, "records": records
    })
