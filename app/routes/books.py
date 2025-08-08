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

@router.get("/")
def list_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "category": b.category,
            "status": b.status,
            "stock_physical_for_sell": b.stock_physical_for_sell,
            "stock_digital": b.stock_digital,
            "min_stock_for_sell": b.min_stock_for_sell,
            "price_physical": b.price_physical,
            "price_digital": b.price_digital,
            "stock_for_loan": b.stock_for_loan
        }
        for b in books
    ]