from app.database import SessionLocal
from app.models.book import Book
from app.models.purchase import Purchase
from datetime import datetime, timedelta, UTC

def decrease_min_stock_for_least_popular_books():
    db = SessionLocal()
    now = datetime.now(UTC)
    six_months_ago = now - timedelta(days=180)
    books = db.query(Book).all()
    for book in books:
        purchases_count = db.query(Purchase).filter(
            Purchase.book_id == book.id,
            Purchase.created_at >= six_months_ago
        ).count()
        if purchases_count == 0:
            old_min = book.min_stock_for_sell
            new_min = max(2, old_min - 2)
            book.min_stock_for_sell = new_min
            print(f"📉 El libro '{book.title}' no tuvo compras en los últimos 6 meses. Stock mínimo reducido de {old_min} a {new_min}.")
    db.commit()
    db.close()