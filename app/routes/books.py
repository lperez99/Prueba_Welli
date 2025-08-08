# app/routes/books.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.book import Book

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books")
def list_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "category": b.category,
            "status": b.status,
            "stock_physical": b.stock_physical,
            "stock_digital": b.stock_digital,
            "min_stock": b.min_stock,
            "price_physical": b.price_physical,
            "price_digital": b.price_digital
        }
        for b in books
    ]