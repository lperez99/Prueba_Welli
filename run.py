from app.database import SessionLocal, Base, engine
from app.models.user import User, UserType
from app.models.book import Book, BookStatus, BookCategory
from app.models.loan import Loan, LoanStatus
from app.models.reservation import Reservation, StatusReservation
from app.models.purchase import Purchase, PurchaseType, PurchaseStatus
from datetime import date, timedelta, datetime, UTC
from random import choice, randint

# -------------------- CREAR TABLAS --------------------
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# -------------------- USUARIOS DE EJEMPLO --------------------
sample_users = [
    {"name": "Alice Johnson", "type": UserType.student, "fines": 0.0, "books_on_loan": 1},
    {"name": "Bob Smith", "type": UserType.teacher, "fines": 0.0, "books_on_loan": 2},
    {"name": "Carlos Pérez", "type": UserType.visitor, "fines": 0.0, "books_on_loan": 0},
    {"name": "Daniela Ruiz", "type": UserType.student, "fines": 0.0, "books_on_loan": 3},
    {"name": "Elena Gómez", "type": UserType.teacher, "fines": 0.0, "books_on_loan": 5},
    {"name": "Sandra Castillo", "type": UserType.student, "fines": 30000.0, "books_on_loan": 0},
    {"name": "Alejandro Gómez", "type": UserType.teacher, "fines": 0.0, "books_on_loan": 4},
]

# -------------------- LIBROS DE EJEMPLO --------------------
sample_books = [
    {
        "title": "Introducción a la Programación avanzada",
        "author": "Juan Pérez",
        "category": BookCategory.academic,
        "status": BookStatus.available,
        "stock_physical_for_sell": 2,
        "min_stock_for_sell": 5,
        "price_physical": 25000.0,
        "price_digital": 15000.0,
        "stock_for_loan": 0
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
        "title": "Historia de Colombia",
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
        "title": "Introducción a la Programación 1",
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

# -------------------- INSERCIÓN DE LIBROS --------------------
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

# -------------------- INSERCIÓN DE USUARIOS --------------------
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
    print("La tabla de usuarios ya tiene datos.")

# -------------------- INSERCIÓN DE PRÉSTAMOS --------------------
if db.query(Loan).count() == 0:
    users = db.query(User).all()
    books = db.query(Book).all()

    LOAN_DAYS = {
        "student": 14,
        "teacher": 30,
        "visitor": 7
    }

    # Préstamos activos
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

    # Préstamos retrasados
    late_loan1 = Loan(
        user_id=users[3].id,
        book_id=books[3].id,
        start_date=date.today() - timedelta(days=20),
        end_date=date.today() - timedelta(days=10),
        returned=False,
        extended=False,
        status=LoanStatus.active
    )
    late_loan2 = Loan(
        user_id=users[4].id,
        book_id=books[4].id,
        start_date=date.today() - timedelta(days=40),
        end_date=date.today() - timedelta(days=31),
        returned=False,
        extended=False,
        status=LoanStatus.active
    )
    db.add(late_loan1)
    db.add(late_loan2)
    db.commit()
    print("Préstamos insertados correctamente ✅")
else:
    print("La tabla de préstamos ya tiene datos.")

# -------------------- INSERCIÓN DE RESERVAS --------------------
if db.query(Reservation).count() == 0:
    users = db.query(User).all()
    books = db.query(Book).all()
    reservation1 = Reservation(
        user_id=users[0].id,
        book_id=books[1].id,
        status=StatusReservation.pending
    )
    reservation2 = Reservation(
        user_id=users[1].id,
        book_id=books[0].id,
        status=StatusReservation.pending
    )
    db.add(reservation1)
    db.add(reservation2)
    db.commit()
    print("Reservas insertadas correctamente ✅")
else:
    print("La tabla de reservas ya tiene datos.")

# -------------------- INSERCIÓN DE COMPRAS --------------------
if db.query(Purchase).count() == 0:
    users = db.query(User).all()
    books = db.query(Book).all()

    # Compras de ejemplo
    purchases = [
        Purchase(
            user_id=users[0].id,
            book_id=books[0].id,
            quantity=2,
            total_price=books[0].price_physical * 2,
            type=PurchaseType.physical,
            status=PurchaseStatus.approved
        ),
        Purchase(
            user_id=users[1].id,
            book_id=books[1].id,
            quantity=1,
            total_price=books[1].price_digital,
            type=PurchaseType.digital,
            status=PurchaseStatus.pending
        ),
        Purchase(
            user_id=users[2].id,
            book_id=books[0].id,
            quantity=3,
            total_price=books[2].price_physical * 3,
            type=PurchaseType.physical,
            status=PurchaseStatus.pending
        ),
    ]
    db.add_all(purchases)
    db.commit()
    print("Compras insertadas correctamente ✅")

    # --- COMPRAS FICTICIAS PARA 'Cuentos Fantásticos' ---
    now = datetime.now(UTC)
    cuentos = books[1]  # "Cuentos Fantásticos"
    fake_purchases = []
    for i in range(12):
        fake_purchases.append(
            Purchase(
                user_id=users[i % len(users)].id,
                book_id=cuentos.id,
                quantity=1,
                total_price=cuentos.price_physical,
                type=PurchaseType.physical,
                status=PurchaseStatus.approved,
                created_at=now - timedelta(days=i * 2),
                reserved_until=None
            )
        )
    db.add_all(fake_purchases)
    db.commit()
    print("Compras ficticias para 'Cuentos Fantásticos' creadas para pruebas de popularidad.")

    # --- MÁS COMPRAS FICTICIAS VARIADAS ---
    matematicas = next(b for b in books if b.title == "Matemáticas Avanzadas")
    cuentos = next(b for b in books if b.title == "Cuentos Fantásticos")
    prohibido = next(b for b in books if b.title == "Introducción a la Programación 1")
    otros_libros = [b for b in books if b.id not in [prohibido.id]]

    tipos = [PurchaseType.physical, PurchaseType.digital]
    fake_purchases_varias = []
    now = datetime.now(UTC)

    for i in range(30):
        if i % 3 == 0:
            libro = cuentos
        elif i % 3 == 1:
            libro = matematicas
        else:
            libro = choice([b for b in otros_libros if b.id not in [cuentos.id, matematicas.id]])
        tipo = choice(tipos)
        precio = libro.price_physical if tipo == PurchaseType.physical else libro.price_digital
        fake_purchases_varias.append(
            Purchase(
                user_id=users[i % len(users)].id,
                book_id=libro.id,
                quantity=randint(1, 3),
                total_price=precio,
                type=tipo,
                status=PurchaseStatus.approved,
                created_at=now - timedelta(days=randint(0, 29)),
                reserved_until=None
            )
        )
    db.add_all(fake_purchases_varias)
    db.commit()
    print("30 compras ficticias variadas creadas (sin compras para 'Introducción a la Programación 1').")
else:
    print("La tabla de compras ya tiene datos.")

db.close()