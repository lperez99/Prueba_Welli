from fastapi import FastAPI
from app.api import users, books, loans, purchases


app = FastAPI(title="Digital Library API")

app.include_router(users.router, prefix="/users")
app.include_router(books.router, prefix="/books")
app.include_router(loans.router, prefix="/loans")
app.include_router(purchases.router, prefix="/purchases")

@app.get("/")
def root():
    return {"message": "API de Biblioteca lista 🚀"}
