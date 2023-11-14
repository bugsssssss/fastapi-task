from fastapi import HTTPException
from database import SessionLocal, User, password_context
from models import UserUpdate


def create_user_method(db, user: User):
    try:
        hashed_password = password_context.hash(user.password)
        db_user = User(full_name=user.full_name,
                       username=user.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        return {'db_error': str(e)}


def get_user_method(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def get_all_users_method(db):
    try:
        return db.query(User).all()
    except Exception as e:
        return {'db_error': str(e)}


def update_user_method(db, user_id: int, updated_user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in updated_user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return {
            'id': db_user.id,
            'full_name': db_user.full_name,
            'username': db_user.username
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


def delete_user_method(db, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


def get_user_by_username_method(db, username: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return {
            'id': db_user.id,
            'full_name': db_user.full_name,
            'username': db_user.username,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
