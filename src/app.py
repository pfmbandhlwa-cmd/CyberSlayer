import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.database import init_db
from src.routes import admin, ai_mentor, auth, badges, challenges, dashboard, scanner

app = FastAPI(title="CyberSlayer API")

# Initialize database on app startup
init_db()

# Mount frontend static files
app.mount("/static", StaticFiles(directory="web"), name="static")

# Register modular routes
app.include_router(auth.router)
app.include_router(challenges.router)
app.include_router(scanner.router)
app.include_router(ai_mentor.router)
app.include_router(dashboard.router)
app.include_router(badges.router)
app.include_router(admin.router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join("web", "index.html")
    with open(index_path, "r") as f:
        return f.read()
