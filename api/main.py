import sys

import logging
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
    logging.getLogger('passlib').setLevel(logging.ERROR)  # disables passlib warning about bcrypt (__about__ not exist) 
    if (len(sys.argv) < 3):
        raise Exception("Address and port are not provided")
    uvicorn.run(app, host=sys.argv[1], port=int(sys.argv[2]))

# export DB_CONNECTION="sqlite:///./database.db"
# export SECRET_KEY="91164f112606672942e9a66658649af033c501586b348f226d2f56b2e23bb135"
# export ALGORITHM="HS256"