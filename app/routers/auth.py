from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.auth import create_access_token  # Génère le token JWT
from app.schemas.user import UserInscriptionReurn  # Réponse avec token
from app.utils.security import verify_password  # importer la fonction de vérification

router = APIRouter(prefix="/v1/login", tags=["Auth"])

@router.post("/", response_model=UserInscriptionReurn, summary="Se connecter")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Se connecter avec un email et un mot de passe.
    
    Si les informations sont correctes, une clé JWT est générée et retournée.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email, "status": user.status.value})
    return {"token": token}
