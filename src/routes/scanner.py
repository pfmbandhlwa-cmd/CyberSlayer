import socket
import ssl
import urllib.request
from datetime import datetime

from fastapi import APIRouter
from src.services.scanner_service import scanner_service

router = APIRouter(tags=["Scanner & Diagnostics"])

@router.get("/run")
def run_diagnostic(target: str = "127.0.0.1"):
    return {"result": scanner_service.execute_scan(target)}

@router.get("/logs")
def fetch_logs():
    return {"logs": scanner_service.get_logs()}

@router.delete("/logs")
def clear_logs():
    scanner_service.clear_logs()
    return {"message": "Execution history cleared successfully"}

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Alt"
}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]

def scan_ports(host: str, timeout: float = 1.0) -> list:
    results = []
    for port, service in COMMON_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            res = sock.connect_ex((host, port))
            state = "OPEN" if res == 0 else "CLOSED"
        except Exception:
            state = "ERROR"
        finally:
            sock.close()
        results.append({"port": port, "service": service, "state": state})
    return results

def audit_http_headers(host: str) -> dict:
    url = host if host.startswith("http") else f"https://{host}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CyberSlayer/1.0'})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            headers = resp.headers
            found = {h: headers[h] for h in SECURITY_HEADERS if h in headers}
            missing = [h for h in SECURITY_HEADERS if h not in headers]
            return {"status": "SUCCESS", "found": found, "missing": missing}
    except Exception as e:
        return {"status": "FAILED", "error": str(e), "found": {}, "missing": SECURITY_HEADERS}

def inspect_ssl_cert(host: str) -> dict:
    # Strip protocols if present
    clean_host = host.replace("https://", "").replace("http://", "").split("/")[0]
    ctx = ssl.create_default_context()
    
    try:
        with socket.create_connection((clean_host, 443), timeout=3.0) as sock:
            with ctx.wrap_socket(sock, server_hostname=clean_host) as ssock:
                cert = ssock.getpeercert()
                
                not_after_str = cert.get('notAfter')
                expiry_date = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.utcnow()).days
                
                issuer = dict(x[0] for x in cert.get('issuer', []))
                
                return {
                    "status": "VALID",
                    "issuer": issuer.get('organizationName', 'Unknown'),
                    "expires_on": expiry_date.strftime('%Y-%m-%d'),
                    "days_remaining": days_left,
                    "is_expired": days_left < 0
                }
    except Exception as e:
        return {"status": "FAILED", "error": str(e)}
