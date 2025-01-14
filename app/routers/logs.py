from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.log import Log
from app.schemas.log import LogCreate, LogResponse

router = APIRouter(prefix="/v1/logs", tags=["Logs"])

@router.post("/", response_model=LogResponse, status_code=201)
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/{id}", response_model=LogResponse)
def get_log(id: int, db: Session = Depends(get_db)):
    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
