from datetime import UTC, datetime
from sqlalchemy.orm import Session
from app.db.models import ETLRun

class ETLRunRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def start(self) -> ETLRun:
        run = ETLRun(status="RUNNING", started_at=datetime.now(UTC))
        self.db.add(run)
        self.db.flush()
        return run
    
    def finish(self, run: ETLRun, rows_processed: int) -> None:
        run.status = "SUCCESS"
        run.rows_processed = rows_processed
        run.finished_at = datetime.now(UTC)
        
    def fail(self, run: ETLRun, error: Exception) -> None:
        run.status = "FAILED"
        run.finished_at = datetime.now(UTC)
        run.error = str(error)