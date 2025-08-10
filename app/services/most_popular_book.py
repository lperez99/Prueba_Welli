from app.database import SessionLocal
from app.models.book import Book
from app.models.purchase import Purchase
from datetime import datetime, timedelta, UTC

def increase_min_stock_for_popular_books():
    db = SessionLocal()
    now = datetime.now(UTC)
    one_month_ago = now - timedelta(days=30)
    books = db.query(Book).all()
    for book in books:
        count = db.query(Purchase).filter(
            Purchase.book_id == book.id,
            Purchase.created_at >= one_month_ago
        ).count()
        if count > 10:
            old_min = book.min_stock_for_sell
            book.min_stock_for_sell += 3
            print(f"📈 El libro '{book.title}' tuvo {count} compras (físicas o digitales) en el último mes. Stock mínimo aumentado de {old_min} a {book.min_stock_for_sell}.")
    db.commit()
    db.close()