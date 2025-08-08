from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, type=user.type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()
