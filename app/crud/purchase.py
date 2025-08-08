from app.models.purchase import Purchase, PurchaseType
from app.models.user import User
from app.models.book import Book, BookCategory
from sqlalchemy.orm import Session

def create_purchase(db: Session, data):
    user = db.query(User).filter(User.id == data.user_id).first()
    book = db.query(Book).filter(Book.id == data.book_id).first()
    
    if not user or not book:
        raise ValueError("Usuario o libro no encontrado.")

    if user.fines > 20000:
        raise ValueError("No puedes comprar con multas mayores a $20.000.")

    from app.models.loan import Loan, LoanStatus
    active_loan = db.query(Loan).filter(
        Loan.user_id == user.id,
        Loan.book_id == book.id,
        Loan.status == LoanStatus.active
    ).first()
    if active_loan:
        raise ValueError("No puedes comprar un libro que tienes prestado actualmente.")

    
    if data.type == "physical":
        if book.stock_physical_for_sell < data.quantity:
            raise ValueError("No hay suficiente stock físico.")
        book.stock_physical_for_sell -= data.quantity
        price = book.price_physical
        if book.stock_physical_for_sell <= book.min_stock_for_sell:
            print(f"⚠️ Advertencia: El stock físico del libro '{book.title}' está por debajo del mínimo. No olvides ordenar mas ejemplares.")
    elif data.type == "digital":
        price = book.price_digital
    else:
        raise ValueError("Tipo de compra inválido.")
    
    # Descuentos por volumen
    discount = 0
    if data.quantity > 5:
        discount += 0.15
    elif data.quantity > 3:
        discount += 0.10

    # Descuento especial para profesores en libros académicos
    if user.type == "teacher" and book.category == BookCategory.academic:
        discount += 0.20
    if user.type == "student" and data.type == "digital":
        discount += 0.15
        
    

    total_price = price * data.quantity * (1 - discount)

    purchase = Purchase(
        user_id=user.id,
        book_id=book.id,
        quantity=data.quantity,
        total_price=total_price,
        type=data.type
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase