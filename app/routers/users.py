from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserInscriptionReurn, UserResponse, UserBase, UserUpdate
from app.auth import create_access_token
from app.models.enum import EquipmentEnum, RoleEnum
from app.dependencies import get_current_user, admin_required
from typing import List
from app.models.boat import Boat
from app.schemas.boat import BoatResponse
from app.utils.security import hash_password  # importer la fonction de hash

router = APIRouter(prefix="/v1/users", tags=["Users"])

@router.post("/", response_model=UserInscriptionReurn, status_code=201)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    # Vérifier l'existence de l'utilisateur
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hacher le mot de passe
    user_data = user.dict()
    if user_data.get("password"):
        user_data["password"] = hash_password(user_data["password"])
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token(data={"sub": db_user.email, "status": db_user.status.value})
    return {"token": token}

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}", response_model=UserResponse)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        print("User not found", id)
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the current user is either the user being updated or an admin
    if current_user.id != user.id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not enough permissions to update this user")
    
    # If the update contains the role, ensure the current user is an admin
    if 'role' in user_update.dict() and user_update.dict()['role'] is not None and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update the role")

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}", response_model=dict)
def delete_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    # Seul un admin peut supprimer un utilisateur
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/me/boats", response_model=List[BoatResponse])
def list_user_boats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    boats = db.query(Boat).filter(Boat.owner_id == current_user.id).all()
    
    # Ensure equipment is a list
    for boat in boats:
        if isinstance(boat.equipment, str):
            boat.equipment = boat.equipment.split(',')
        if isinstance(boat.equipment, list):
            boat.equipment = [item.strip() for item in boat.equipment if item.strip() in [e.value for e in EquipmentEnum]]
    
    return boats