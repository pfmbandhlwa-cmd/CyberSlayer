from datetime import datetime
import logging
from src.services.scanner_service import scan_ports, audit_http_headers, inspect_ssl_cert

logger = logging.getLogger("cyberslayer.scanner")

def run_cyberslayer(target: str = "example.com") -> dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Clean the target URL/hostname
    clean_target = (
        target.replace("https://", "")
              .replace("http://", "")
              .split("/")[0]  # Strips any subpaths like /login
              .strip()
    )
    
    if not clean_target:
        clean_target = "127.0.0.1"

    # 2. Run port scan with fallback
    try:
        ports_res = scan_ports(clean_target)
    except Exception as e:
        logger.error(f"Port scan failed for {clean_target}: {e}")
        ports_res = {"error": f"Port scan failed: {str(e)}"}

    # 3. Run HTTP header audit with fallback
    try:
        headers_res = audit_http_headers(clean_target)
    except Exception as e:
        logger.error(f"Header audit failed for {clean_target}: {e}")
        headers_res = {"error": f"Header audit failed: {str(e)}"}

    # 4. Run SSL inspection with fallback
    try:
        ssl_res = inspect_ssl_cert(clean_target)
    except Exception as e:
        logger.error(f"SSL inspection failed for {clean_target}: {e}")
        ssl_res = {"error": f"SSL inspection failed: {str(e)}"}

    return {
        "target": clean_target,
        "status": "COMPLETED",
        "timestamp": timestamp,
        "ports": ports_res,
        "header_audit": headers_res,
        "ssl_audit": ssl_res
    }