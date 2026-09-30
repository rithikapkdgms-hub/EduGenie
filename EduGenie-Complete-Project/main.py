"""EduGenie: a small FastAPI learning assistant."""
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

import explanation_module
import learning_path
import qna
import quiz_module
import summary_module

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="EduGenie", description="An AI-powered learning assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TaskRequest(BaseModel):
    text: str = Field(min_length=2, max_length=20000)
    level: str = Field(default="Beginner", max_length=40)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


async def execute(operation, text: str, level: str = "Beginner"):
    try:
        return await operation(text, level) if operation is learning_path.get_learning_recommendations else await operation(text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI request failed: {exc}") from exc


@app.post("/qa")
async def answer_question(payload: TaskRequest):
    return {"result": await execute(qna.answer_question, payload.text), "mode": qna.ai_mode()}


@app.post("/explain")
async def explain_concept(payload: TaskRequest):
    return {"result": await execute(explanation_module.explain_concept, payload.text), "mode": explanation_module.ai_mode()}


@app.post("/quiz")
async def generate_quiz(payload: TaskRequest):
    return {"result": await execute(quiz_module.generate_quiz, payload.text), "mode": quiz_module.ai_mode()}


@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return {"result": await execute(summary_module.summarize_text, payload.text), "mode": summary_module.ai_mode()}


@app.post("/learn/recommendations")
async def recommend_learning(payload: TaskRequest):
    return {"result": await execute(learning_path.get_learning_recommendations, payload.text, payload.level), "mode": learning_path.ai_mode()}
