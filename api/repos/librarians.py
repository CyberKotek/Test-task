import sys
sys.path.append("../")

from typing import List
from fastapi import APIRouter, Depends
import schemas, database, models
from sqlalchemy.orm import Session
from hashing import Hash


async def create_librarian(request: schemas.Librarian, db: Session = Depends(database.get_db)):
    new_librarian = models.Librarians(email=request.email, password=Hash.get_hash(request.password))
    db.add(new_librarian)
    db.commit()
    db.refresh(new_librarian)
    return new_librarian