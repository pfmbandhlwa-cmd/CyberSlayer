import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyberslayer.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Scanner execution log storage
EXECUTION_LOGS = []

def log_execution(target: str, scan_type: str, status: str = "completed", details: str = ""):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "target": target,
        "scan_type": scan_type,
        "status": status,
        "details": details
    }
    EXECUTION_LOGS.append(log_entry)
    return log_entry

def get_all_logs():
    return EXECUTION_LOGS

def clear_all_logs():
    EXECUTION_LOGS.clear()
    return True

def get_db():
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Imports ORM models and creates all tables in SQLite."""
    import src.models.challenge
    import src.models.user
    import src.models.progress
    Base.metadata.create_all(bind=engine)
