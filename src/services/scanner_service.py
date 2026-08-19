
from src.database.db import log_execution, get_all_logs, clear_all_logs

class ScannerService:
    from src.main import run_cyberslayer
    def execute_scan(self, target: str):
        result = run_cyberslayer(target)
        log_execution(
            target=result.get("target", target),
            status=result.get("status", "Executed"),
            timestamp=result.get("timestamp", "")
        )
        return result

    def get_logs(self):
        return get_all_logs()

    def clear_logs(self):
        clear_all_logs()

scanner_service = ScannerService()