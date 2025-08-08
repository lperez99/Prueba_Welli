from app.database import SessionLocal, Base, engine
from app.models.user import User, UserType
from app.models.book import Book, BookStatus, BookCategory
from app.models.loan import Loan, LoanStatus
from datetime import date, timedelta

# Crear tablas
Base.metadata.create_all(bind=engine)

# Sesión de DB
db = SessionLocal()

# Insertar datos de ejemplo
sample_users = [
    {"name": "Alice Johnson", "type": UserType.student, "fines": 0.0, "books_on_loan": 1},
    {"name": "Bob Smith", "type": UserType.teacher, "fines": 0.0, "books_on_loan": 2},
    {"name": "Carlos Pérez", "type": UserType.visitor, "fines": 0.0, "books_on_loan": 0},
    # {"name": "Daniela Ruiz", "type": UserType.student, "fines": 0.0, "books_on_loan": 3},
    # {"name": "Elena Gómez", "type": UserType.teacher, "fines": 0.0, "books_on_loan": 5},
]
sample_books = [
    {
        "title": "Introducción a la Programación",
        "author": "Juan Pérez",
        "category": BookCategory.academic,
        "status": BookStatus.available,
        "stock_physical_for_sell": 2,
        "min_stock_for_sell": 5,
        "price_physical": 25000.0,
        "price_digital": 15000.0,
        "stock_for_loan": 5
    },
    {
        "title": "Cuentos Fantásticos",
        "author": "María López",
        "category": BookCategory.fiction,
        "status": BookStatus.available,
        "stock_physical_for_sell": 3,
        "min_stock_for_sell": 2,
        "price_physical": 18000.0,
        "price_digital": 12000.0,
        "stock_for_loan": 2
    },
    {
        "title": "Historia de Chile",
        "author": "Pedro González",
        "category": BookCategory.history,
        "status": BookStatus.maintenance,
        "stock_physical_for_sell": 0,
        "min_stock_for_sell": 3,
        "price_physical": 30000.0,
        "price_digital": 20000.0,
        "stock_for_loan": 0
    },
    {
        "title": "Matemáticas Avanzadas",
        "author": "Laura Martínez",
        "category": BookCategory.academic,
        "status": BookStatus.available,
        "stock_physical_for_sell": 7,
        "min_stock_for_sell": 4,
        "price_physical": 35000.0,
        "price_digital": 22000.0,
        "stock_for_loan": 3
    },
    {
        "title": "Introducción a la Programación",
        "author": "Juan Pérez",
        "category": BookCategory.academic,
        "status": BookStatus.available,
        "stock_physical_for_sell": 10,
        "min_stock_for_sell": 5,
        "price_physical": 25000.0,
        "price_digital": 15000.0,
        "stock_for_loan": 5
    },
    {
        "title": "Introducción a la Programación",
        "author": "Juan Pérez",
        "category": BookCategory.academic,
        "status": BookStatus.available,
        "stock_physical_for_sell": 10,
        "min_stock_for_sell": 5,
        "price_physical": 25000.0,
        "price_digital": 15000.0,
        "stock_for_loan": 1
    },
]

if db.query(Book).count() == 0:
    for b in sample_books:
        book = Book(
            title=b["title"],
            author=b["author"],
            category=b["category"],
            status=b["status"],
            stock_physical_for_sell=b["stock_physical_for_sell"],
            min_stock_for_sell=b["min_stock_for_sell"],
            price_physical=b["price_physical"],
            price_digital=b["price_digital"],
            stock_for_loan=b["stock_for_loan"]
        )
        db.add(book)
    db.commit()
    print("Libros insertados correctamente ✅")
else:
    print("La tabla de libros ya tiene datos.")



if db.query(User).count() == 0:
    for u in sample_users:
        user = User(
            name=u["name"],
            type=u["type"],
            fines=u["fines"],
            books_on_loan=u["books_on_loan"]
        )
        db.add(user)
    db.commit()
    print("Usuarios insertados correctamente ✅")
else:
    print("La tabla ya tiene datos, no se insertó nada.")

db.close()

if db.query(Loan).count() == 0:
    users = db.query(User).all()
    books = db.query(Book).all()

    # Diccionario de días por tipo de usuario
    LOAN_DAYS = {
        "student": 14,
        "teacher": 30,
        "visitor": 7
    }

    sample_loans = [
        {"user": users[0], "book": books[0], "returned": False, "extended": False, "status": LoanStatus.active},
        {"user": users[1], "book": books[1], "returned": False, "extended": False, "status": LoanStatus.active},
        {"user": users[2], "book": books[2], "returned": False, "extended": False, "status": LoanStatus.active}
    ]

    for l in sample_loans:
        user_type = getattr(l["user"], "type", None) or "visitor"
        loan_days = LOAN_DAYS.get(user_type, LOAN_DAYS["visitor"])

        loan = Loan(
            user_id=l["user"].id,
            book_id=l["book"].id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=loan_days),
            returned=l["returned"],
            extended=l["extended"],
            status=l["status"]
        )
        db.add(loan)
    db.commit()
    print("Préstamos insertados correctamente ✅")
else:
    print("La tabla de préstamos ya tiene datos.")