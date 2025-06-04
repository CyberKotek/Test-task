from typing import List
from datetime import datetime
from pydantic import BaseModel



class Librarian(BaseModel):
    email: str
    name: str
    password: str

class Reader(BaseModel):
    name: str
    email: str

class Book(BaseModel):
    name: str
    author: str
    published_year: int | None = None
    isbn: str | None = None
    amount: int = 1

class Borrow(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: datetime | None = None
    # class Config():
    #     orm_mode = True

class ReturnedBorrow(Borrow):
    return_date: datetime



class ShowLibrarian(BaseModel):
    id: int
    email: str
    password: str

class ShowReader(Reader):
    id: int
    class Config():
        orm_mode = True

class ShowBook(Book):
    id: int
    class Config():
        orm_mode = True

class ShowBorrow(BaseModel):
    id: int
    book: ShowBook
    reader: ShowReader
    borrow_date: datetime

    class Config():
        orm_mode = True

class ShowBorrowOnlyBook(BaseModel):
    id: int
    book: ShowBook
    reader_id: int
    borrow_date: datetime

class ShowBorrowOnlyReader(BaseModel):
    id: int
    book_id: int
    reader: ShowReader
    borrow_date: datetime

class ShowReturnedBorrow(BaseModel):
    id: int
    book: ShowBook
    reader: ShowReader
    borrow_date: datetime
    return_date: datetime
    class Config():
        orm_mode = True

class ShowOnlyReader(ShowReader):
    borrows: List[ShowBorrowOnlyBook] = []
    class Config():
        orm_mode = True
 
class ShowOnlyBook(ShowBook):
    borrows: List[ShowBorrowOnlyReader] = []
    class Config():
        orm_mode = True



class FindReader(BaseModel):
    id: int | None = None
    name: str | None = None
    email: str | None = None

class FindBook(BaseModel):
    id: int | None = None
    name: str | None = None
    author: str | None = None
    published_year: int | None = None
    isbn: str | None = None
    amount: int | None = None

class FindBorrow(BaseModel):
    id: int | None = None
    book_id: int | None = None
    reader_id: int | None = None

class FindReturnedBorrow(FindBorrow):
    return_date : datetime | None = None



class OauthForm(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None