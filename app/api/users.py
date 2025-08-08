from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schema.user import UserCreate, UserOut
from app.crud import user as user_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/", response_model=UserOut)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     return user_crud.create_user(db, user)

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)
