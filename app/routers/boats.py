from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.boat import Boat
from app.schemas.boat import BoatCreate, BoatResponse

router = APIRouter(prefix="/v1/boats", tags=["Boats"])

@router.post("/", response_model=BoatResponse, status_code=201)
def create_boat(boat: BoatCreate, db: Session = Depends(get_db)):
    db_boat = Boat(**boat.dict())
    db.add(db_boat)
    db.commit()
    db.refresh(db_boat)
    return db_boat

@router.get("/{id}", response_model=BoatResponse)
def get_boat(id: int, db: Session = Depends(get_db)):
    boat = db.query(Boat).filter(Boat.id == id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    return boat

@router.put("/{id}", response_model=BoatResponse)
def update_boat(id: int, boat_update: BoatCreate, db: Session = Depends(get_db)):
    boat = db.query(Boat).filter(Boat.id == id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    for key, value in boat_update.dict().items():
        setattr(boat, key, value)
    db.commit()
    db.refresh(boat)
    return boat

@router.delete("/{id}", response_model=dict)
def delete_boat(id: int, db: Session = Depends(get_db)):
    boat = db.query(Boat).filter(Boat.id == id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    db.delete(boat)
    db.commit()
    return {"message": "Boat deleted"}
