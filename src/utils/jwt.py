import base64
import json
from datetime import datetime, timedelta

SECRET_KEY = "cyberslayer-secret-key-change-in-production"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": int(expire.timestamp())})
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    return f"mock_jwt.{encoded}"

def decode_access_token(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return {}
        decoded_bytes = base64.b64decode(parts[1])
        return json.loads(decoded_bytes.decode())
    except Exception:
        return {}
