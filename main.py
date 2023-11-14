from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Union
from database import SessionLocal
from models import UserCreate, UserUpdate
from utils import create_user_method, get_user_method, get_all_users_method, update_user_method, delete_user_method, get_user_by_username_method


app = FastAPI()


# Новая сессия бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание пользователя
@app.post("/users/")
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_method(db, user)


# Получение пользователя по id
@app.get('/users/{user_id}')
async def get_user_detail(user_id, db: Session = Depends(get_db)):
    try:
        user = get_user_method(db, user_id)
        return {'user_id': user.id, 'username': user.username}
    except:
        return {'error': 'user not found'}


# Получение всех пользователей если с username, то одного пользователя

@app.get('/users/')
async def get_users_method(username: Union[str, None] = None, db: Session = Depends(get_db)):
    if username:
        return get_user_by_username_method(db, username)
    else:
        users = get_all_users_method(db)
        users_arr = [
            {
                'id': x.id,
                'username': x.username,
                'full_name': x.full_name
            } for x in users
        ]
        return users_arr


# Обновление пользователя по id


@app.put('/users/{user_id}')
async def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    return update_user_method(db, user_id, updated_user)


# Удаление пользователя по id

@app.delete('/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user_method(db, user_id)
