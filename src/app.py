from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from src.main import run_cyberslayer
from src.db import (
    init_db, log_execution, get_all_logs, clear_all_logs,
    get_all_challenges, check_challenge_answer, add_custom_challenge,
    get_challenge_stats
)

app = FastAPI(title="CyberSlayer API")

init_db()

app.mount("/static", StaticFiles(directory="web"), name="static")

class AnswerSubmission(BaseModel):
    challenge_id: int
    selected_option: str

class ChallengeCreate(BaseModel):
    title: str
    category: str
    difficulty: str
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    hint: str
    explanation: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join("web", "index.html")
    with open(index_path, "r") as f:
        return f.read()

@app.get("/run")
def run_diagnostic(target: str = "127.0.0.1"):
    result = run_cyberslayer(target)
    log_execution(
        target=result.get("target", target),
        status=result.get("status", "Executed"),
        timestamp=result.get("timestamp", "")
    )
    return {"result": result}

@app.get("/logs")
def fetch_logs():
    return {"logs": get_all_logs()}

@app.delete("/logs")
def clear_logs():
    clear_all_logs()
    return {"message": "Execution history cleared successfully"}

@app.get("/challenges")
def fetch_challenges():
    import sqlite3
    conn = sqlite3.connect("cyberslayer.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenges")
    rows = cursor.fetchall()
    challenges = [dict(row) for row in rows]
    conn.close()
    return {"challenges": challenges}
@app.get("/stats")
def fetch_stats():
    """Endpoint for user progress dashboard metrics."""
    return get_challenge_stats()

@app.post("/challenges")
def create_challenge(challenge: ChallengeCreate):
    if challenge.correct_option.upper() not in ["A", "B", "C", "D"]:
        raise HTTPException(status_code=400, detail="Correct option must be A, B, C, or D")
        
    new_id = add_custom_challenge(challenge.model_dump())
    return {"status": "SUCCESS", "message": "Challenge added successfully", "challenge_id": new_id}

@app.post("/challenges/{challenge_id}/submit")
def submit_answer(challenge_id: int, submission: AnswerSubmission):
    result = check_challenge_answer(submission.challenge_id, submission.selected_option)
    return result

@app.post("/answer")
def submit_answer(challenge_id: int, submission: AnswerSubmission):
    result = check_challenge_answer(submission.challenge_id, submission.selected_option)
    return result
