from fastapi import FastAPI
from database import engine, get_db
import models
import uvicorn
from router import librarians, readers, authentification, books, register, borrows, history


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(librarians.router)
app.include_router(readers.router)
app.include_router(books.router)
app.include_router(authentification.router)
app.include_router(register.router)
app.include_router(borrows.router)
app.include_router(history.router)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
