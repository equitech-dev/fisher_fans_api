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
not_found_error_log = "Log not found"
@router.post("/", response_model=LogResponse, summary="Créer une nouvelle page du carnet de pêche")
def create_log(log: LogCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Créer une nouvelle page du carnet de pêche

    Args:
    - log (LogCreate): données de la page à créer

    Returns:
    - LogResponse: La page créée
    """

    db_log = Log(**log.dict(), user_id=current_user.id)
    
    try:
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_log

@router.get("/filter", response_model=List[LogResponse], summary="Filtrer les pages du carnet de pêche")
def filter_logs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    user_id: Optional[int] = Query(None, description="ID de l'utilisateur"),
    fish_name: Optional[str] = Query(None, description="Nom du poisson"),
    min_size: Optional[float] = Query(None, description="Taille minimale"),
    min_weight: Optional[float] = Query(None, description="Poids minimal"),
    location: Optional[str] = Query(None, description="Lieu de pêche"),
    start_date: Optional[date] = Query(None, description="Date de début"),
    end_date: Optional[date] = Query(None, description="Date de fin"),
    released: Optional[bool] = Query(None, description="Vrai si le poisson a été relâché")
):
    """Filtrer les pages du carnet de pêche

    Args:
    - user_id (int): ID de l'utilisateur
    - fish_name (str): Nom du poisson
    - min_size (float): Taille minimale
    - min_weight (float): Poids minimal
    - location (str): Lieu de pêche
    - start_date (date): Date de début
    - end_date (date): Date de fin
    - released (bool): Vrai si le poisson a été relâché

    Returns:
    - List[LogResponse]: La liste des pages filtrées
    """
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

@router.get("/{id}", response_model=LogResponse, summary="Obtenir une page spécifique du carnet de pêche")
def get_log(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Obtenir une page spécifique du carnet de pêche

    Args:
    - id (int): ID de la page

    Returns:
    - LogResponse: La page demandée
    """

    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail=not_found_error_log)
    
    # Vérifier les droits d'accès
    if log.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view this log")
    
    return log

@router.put("/{id}", response_model=LogResponse, summary="Modifier une page du carnet de pêche")
def update_log(
    id: int,
    log_update: LogUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Modifier une page du carnet de pêche

    Args:
    - id (int): ID de la page
    - log_update (LogUpdate): Données de mise à jour

    Returns:
    - LogResponse: La page modifiée
    """

    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail=not_found_error_log)

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

@router.delete("/{id}", summary="Supprimer une page du carnet de pêche")
def delete_log(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Supprimer une page du carnet de pêche

    Args:
    - id (int): ID de la page

    Returns:
    - str: Message de confirmation de suppression
    """

    log = db.query(Log).filter(Log.id == id).first()
    if not log:
        raise HTTPException(status_code=404, detail=not_found_error_log)

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
