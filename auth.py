# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

from database import User, password_context

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Создание jwt токена
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Декодинг jwt токена
def decode_jwt_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception


# Проверка данных логина
def authenticate_user(db, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()

    if db_user:
        if password_context.verify(password, db_user.password):
            return True
    return False


# Получение пользователя по jwt токену
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    if payload['sub']:
        return {'username': payload['sub']}
    else:
        return {'error': 'user not foundr'}
