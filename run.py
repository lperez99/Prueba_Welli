# from app.database import Base, engine, SessionLocal
from app.database import SessionLocal, Base, engine
from app.models.user import User, UserType

# Crear tablas
Base.metadata.create_all(bind=engine)

# Sesión de DB
db = SessionLocal()

# Datos de ejemplo
sample_users = [
    {"name": "Alice Johnson", "type": UserType.student, "fines": 0.0, "books_on_loan": 1},
    {"name": "Bob Smith", "type": UserType.teacher, "fines": 5000.0, "books_on_loan": 2},
    {"name": "Carlos Pérez", "type": UserType.visitor, "fines": 12000.0, "books_on_loan": 0},
    {"name": "Daniela Ruiz", "type": UserType.student, "fines": 0.0, "books_on_loan": 3},
    {"name": "Elena Gómez", "type": UserType.teacher, "fines": 0.0, "books_on_loan": 5},
]

# Insertar solo si no hay datos
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