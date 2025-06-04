import sys
sys.path.append("../")

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import schemas, database, models
from sqlalchemy.orm import Session
import oauth2


router = APIRouter(
    tags=["Books"],
    prefix="/books"
)


@router.get("/", response_model=List[schemas.ShowOnlyBook])
def get_all(db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    return db.query(models.Books).all()


@router.post("/find", response_model=List[schemas.ShowOnlyBook])
def find_all(request: schemas.FindBook, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    querry_dict = {}
    request_dict = request.dict()
    for i in request_dict:
        if (request_dict[i]):
            querry_dict[i] = request_dict[i]

    books = db.query(models.Books).filter_by(**querry_dict).all()
    if (not books):
        raise HTTPException(status_code=404, detail=f"No such book")
    return books


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_book(request: schemas.Book, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    if (request.isbn):
        existing = db.query(models.Books).filter(models.Books.isbn == request.isbn).first()
        if (existing):
            raise HTTPException(status_code=400, detail=f"book with ISBN {request.isbn} already exists")
    if (request.amount < 0):
        raise HTTPException(status_code=400, detail=f"amount can not be less than 0")


    new_book = models.Books(request)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    book = db.query(models.Books).filter(models.Books.id == id).first()
    if (not book):
        raise HTTPException(status_code=400, detail=f"There is no book with such ID")
        
    db.delete(book)
    db.commit()


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def upadte_book(request: schemas.Book, id: int, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    book = db.query(models.Books).filter(models.Books.id == id)
    if (not book.first()):
        raise HTTPException(status_code=400, detail=f"There is no book with such ID")

    book.update(request.dict())
    db.commit()