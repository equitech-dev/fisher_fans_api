from datetime import datetime, timedelta, datetime
import jwt
from app.models.enum import StatusEnum

SECRET_KEY = "FF_API"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "api_key": SECRET_KEY})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
    
def check_payload(payload: dict):
    if payload.get("exp") < datetime.now(timezone.utc):
        raise jwt.ExpiredSignatureError
    if payload.get("api_key") != SECRET_KEY:
        raise jwt.InvalidSignatureError
    if payload.get('sub') is None:
        raise jwt.InvalidTokenError
    if payload.get('status') is not StatusEnum.PARTICULIER.value and payload.get('status') is not StatusEnum.PROFESSIONNEL.value:
        raise jwt.InvalidTokenError
    return True

def check_token(token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise jwt.InvalidTokenError
    return True