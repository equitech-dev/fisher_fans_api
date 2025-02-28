from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.boat import Boat
from app.schemas.boat import BoatCreate, BoatResponse
from app.schemas.boat import BoatUpdate
from app.dependencies import get_current_user  # importer current_user
from app.models.enum import RoleEnum

router = APIRouter(prefix="/v1/boats", tags=["Boats"])
@router.post("/", response_model=dict, status_code=201)
def create_boat(boat: BoatCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Crée un bateau.

    Args:
    - boat (BoatCreate): Informations du bateau.

    Returns:
    - dict: Message de confirmation.
    """
    if not current_user.boat_license:
        raise HTTPException(status_code=403, detail="User must provide boat license to create a boat")
    boat_data = boat.dict()
    if "equipment" in boat_data:
        boat_data["equipment"] = ",".join(boat_data["equipment"])
    db_boat = Boat(**boat_data, owner_id=current_user.id)
    db.add(db_boat)
    db.commit()
    db.refresh(db_boat)
    return {"message": "Boat created successfully"}

@router.get("/filter", response_model=List[BoatResponse])
def filter_boats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    name: Optional[str] = Query(None),
    marque: Optional[str] = Query(None),
    annee_fabrication: Optional[int] = Query(None),
    boat_type: Optional[str] = Query(None, regex="^(open|cabine|catamaran|voilier|jetski|cano )$"),
    min_latitude: Optional[float] = Query(None),
    max_latitude: Optional[float] = Query(None),
    min_longitude: Optional[float] = Query(None),
    max_longitude: Optional[float] = Query(None),
):
    """
    Filtrer les bateaux.

    Args:
    - name (str): Filtre sur le nom du bateau.
    - marque (str): Filtre sur la marque du bateau.
    - annee_fabrication (int): Filtre sur l'année de fabrication du bateau.
    - boat_type (str): Filtre sur le type de bateau.
    - min_latitude (float): Filtre sur la latitude minimale.
    - max_latitude (float): Filtre sur la latitude maximale.
    - min_longitude (float): Filtre sur la longitude minimale.
    - max_longitude (float): Filtre sur la longitude maximale.

    Returns:
    - List[BoatResponse]: Liste des bateaux filtrés.
    """
    query = db.query(Boat)
    if current_user.role != RoleEnum.ADMIN:
        query = query.filter(Boat.owner_id == current_user.id)
    if name:
        query = query.filter(Boat.name.ilike(f"%{name}%"))
    if marque:
        query = query.filter(Boat.marque.ilike(f"%{marque}%"))
    if annee_fabrication:
        query = query.filter(Boat.annee_fabrication == annee_fabrication)
    if boat_type:
        query = query.filter(Boat.boat_type == boat_type)
    if all(param is not None for param in [min_latitude, max_latitude]):
        query = query.filter(Boat.latitude.between(min_latitude, max_latitude))
    if all(param is not None for param in [min_longitude, max_longitude]):
        query = query.filter(Boat.longitude.between(min_longitude, max_longitude))
    data =query.all()
    for boat in data:
        if boat.equipment:
            boat.equipment = boat.equipment.split(",")
    return data

@router.get("/{id}", response_model=BoatResponse)
def get_boat(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Obtenir un bateau.

    Args:
    - id (int): Identifiant du bateau.

    Returns:
    - BoatResponse: Bateau.
    """
    boat = db.query(Boat).filter(Boat.id == id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    if boat.equipment:
        boat.equipment = boat.equipment.split(",")
    return boat

@router.put("/{id}", response_model=BoatResponse)
def update_boat(id: int, boat_update: BoatUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Mettre à jour un bateau.

    Args:
    - id (int): Identifiant du bateau.
    - boat_update (BoatUpdate): Informations du bateau à mettre à jour.

    Returns:
    - BoatResponse: Bateau mis à jour.
    """
    boat = db.query(Boat).filter(Boat.id == id, Boat.owner_id == current_user.id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found or not owned by the current user")
    update_data = boat_update.dict(exclude_unset=True)
    if "equipment" in update_data:
        if isinstance(update_data["equipment"], list):
            update_data["equipment"] = ",".join(update_data["equipment"])
        else:
            update_data["equipment"] = update_data["equipment"]
    for key, value in update_data.items():
        setattr(boat, key, value)
    db.commit()
    db.refresh(boat)
    if boat.equipment:
        boat.equipment = boat.equipment.split(",")
    else:
        boat.equipment = []
    return boat

@router.delete("/{id}", response_model=dict)
def delete_boat(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Supprimer un bateau.

    Args:
    - id (int): Identifiant du bateau.

    Returns:
    - dict: Message de confirmation.
    """
    boat = db.query(Boat).filter(Boat.id == id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    if current_user.role != RoleEnum.ADMIN and boat.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this boat")
    db.delete(boat)
    db.commit()
    return {"message": "Boat deleted"}
