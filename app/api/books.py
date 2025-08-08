from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.book import Book
from app.schema.book import BookOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()