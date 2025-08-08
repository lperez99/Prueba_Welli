from fastapi import FastAPI
# from app.api import book, users
from app.routes import loan, books, users, reservation, purchase


app = FastAPI(title="Digital Library API")

app.include_router(users.router, prefix="/users")
app.include_router(books.router, prefix="/books")
app.include_router(loan.router, prefix="/loans")
app.include_router(reservation.router, prefix="/reservations")
app.include_router(purchase.router, prefix="/purchases")

@app.get("/")
def root():
    return {"message": "API de Biblioteca lista 🚀"}
