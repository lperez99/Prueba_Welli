from sqlalchemy.orm import Session
from app.models.book import Book
from app.schema.book import BookCreate, BookOut

def create_book(db: Session, book: BookCreate):
    db_book = Book(title=book.title,
        author=book.author,
        category=book.category,
        status=book.status,
        stock_physical_for_sell=book.stock_physical_for_sell,
        stock_digital=book.stock_digital,
        min_stock_for_sell=book.min_stock_for_sell,
        price_physical=book.price_physical,
        price_digital=book.price_digital
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(Book).all()
