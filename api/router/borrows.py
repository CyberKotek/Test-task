import sys
sys.path.append("../")

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import schemas, database, models
from sqlalchemy.orm import Session
import oauth2


READER_MAX_BOOKS = 3

router = APIRouter(
    tags=["Borrows"],
    prefix="/borrows"
)


@router.get("/", response_model=List[schemas.ShowBorrow])
def get_all(db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    return db.query(models.Borrows).all()


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_borrow(request: schemas.Borrow, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    reader = db.query(models.Readers).filter(models.Readers.id == request.reader_id).first()
    if (not reader):
        raise HTTPException(status_code=400, detail=f"No reader with Such ID")
    if (len(reader.borrows) >= READER_MAX_BOOKS):
        raise HTTPException(status_code=400, detail=f"This reader has already borrowed {READER_MAX_BOOKS} books")
    
    book = db.query(models.Books).filter(models.Books.id == request.book_id).first()
    if (not book):
        raise HTTPException(status_code=400, detail=f"No book with such ID")
    if (len(book.borrows) >= book.amount):
        raise HTTPException(status_code=400, detail=f"No such books left")

    new_borrow = models.Borrows(request)
    db.add(new_borrow)
    db.commit()


@router.post("/find", response_model=List[schemas.ShowBorrow])
def find_all(request: schemas.FindBorrow, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    querry_dict = {}
    request_dict = request.dict()
    for i in request_dict:
        if (request_dict[i]):
            querry_dict[i] = request_dict[i]

    borrows = db.query(models.Borrows).filter_by(**querry_dict).all()
    if (not borrows):
        raise HTTPException(status_code=404, detail=f"No such borrow")
    return borrows


@router.post("/return", status_code=status.HTTP_204_NO_CONTENT)
def return_book(request: schemas.Borrow, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    borrow = db.query(models.Borrows).filter(models.Borrows.reader_id == request.reader_id, models.Borrows.book_id == request.book_id).order_by(models.Borrows.borrow_date).first()
    if (not borrow):
        raise HTTPException(status_code=400, detail=f"No such borrow operation")

    returned_borrow = models.ReturnedBorrows(borrow)
    db.add(returned_borrow)
    db.delete(borrow)
    db.commit()