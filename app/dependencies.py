from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth import decode_access_token  # Supposez que cette fonction décode et vérifie le token

def get_current_user(Authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(Authorization)  # Doit retourner un dictionnaire contenant "sub" (email)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token invalid: missing email")
    except Exception:
        raise HTTPException(status_code=401, detail="Token verification failed")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user
