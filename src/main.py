from datetime import datetime
from src.scanner import scan_ports, audit_http_headers, inspect_ssl_cert

def run_cyberslayer(target: str = "example.com") -> dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_target = target.replace("https://", "").replace("http://", "").strip("/")
    
    ports_res = scan_ports(clean_target)
    headers_res = audit_http_headers(clean_target)
    ssl_res = inspect_ssl_cert(clean_target)
    
    return {
        "target": clean_target,
        "status": "COMPLETED",
        "timestamp": timestamp,
        "ports": ports_res,
        "header_audit": headers_res,
        "ssl_audit": ssl_res
    }
