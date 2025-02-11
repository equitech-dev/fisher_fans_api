from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.log import Log
from app.schemas.log import LogCreate, LogResponse, LogUpdate
from app.dependencies import get_current_user
from app.models.enum import RoleEnum

router = APIRouter(prefix="/v1/logs", tags=["Logs"])

@router.post("/", response_model=LogResponse)
def create_log(log: LogCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Créer une nouvelle page du carnet de pêche"""
    db_log = Log(**log.dict(), user_id=current_user.id)
    
    try:
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_log

@router.get("/filter", response_model=List[LogResponse])
def filter_logs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    user_id: Optional[int] = Query(None),
    fish_name: Optional[str] = Query(None),
    min_size: Optional[float] = Query(None),
    min_weight: Optional[float] = Query(None),
    location: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    released: Optional[bool] = Query(None)
):
    """Filtrer les pages du carnet de pêche"""
    query = db.query(Log)

    # Si non admin, ne montrer que ses propres logs
    if current_user.role != RoleEnum.ADMIN:
        query = query.filter(Log.user_id == current_user.id)
    elif user_id:
        query = query.filter(Log.user_id == user_id)

    if fish_name:
        query = query.filter(Log.fish_name.ilike(f"%{fish_name}%"))
    if min_size:
        query = query.filter(Log.size >= min_size)
    if min_weight:
        query = query.filter(Log.weight >= min_weight)
    if location:
        query = query.filter(Log.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(Log.catch_date >= start_date)
    if end_date:
        query = query.filter(Log.catch_date <= end_date)
    if released is not None:
        query = query.filter(Log.released == released)

    return query.all()

@router.get("/{id}", response_model=LogResponse)
def get_log(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Obtenir une page spécifique du carnet de pêche"""
    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    # Vérifier les droits d'accès
    if log.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view this log")
    
    return log

@router.put("/{id}", response_model=LogResponse)
def update_log(
    id: int,
    log_update: LogUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Modifier une page du carnet de pêche"""
    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    # Vérifier les droits d'accès
    if log.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to modify this log")

    # Mettre à jour les champs
    for key, value in log_update.dict(exclude_unset=True).items():
        setattr(log, key, value)

    try:
        db.commit()
        db.refresh(log)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return log

@router.delete("/{id}")
def delete_log(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Supprimer une page du carnet de pêche"""
    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    # Vérifier les droits d'accès
    if log.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to delete this log")

    try:
        db.delete(log)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Log successfully deleted"}
