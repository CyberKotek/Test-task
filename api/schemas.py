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
    exists: bool | None = True

class Book(BaseModel):
    name: str
    author: str
    published_year: int | None = None
    isbn: str | None = None
    amount: int = 1
    exists: bool | None = True

class Borrow(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: datetime | None = None
    # class Config():
    #     from_attributes = True

class ReturnedBorrow(Borrow):
    return_date: datetime



class ShowLibrarian(BaseModel):
    id: int
    email: str
    password: str

class ShowReader(Reader):
    id: int
    class Config():
        from_attributes = True

class ShowBook(Book):
    id: int
    class Config():
        from_attributes = True

class ShowBorrow(BaseModel):
    id: int
    book: ShowBook
    reader: ShowReader
    borrow_date: datetime
    class Config():
        from_attributes = True

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
        from_attributes = True

class ShowOnlyReader(ShowReader):
    borrows: List[ShowBorrowOnlyBook] = []

 
class ShowOnlyBook(ShowBook):
    borrows: List[ShowBorrowOnlyReader] = []



class FindReader(BaseModel):
    id: int | None = None
    name: str | None = None
    email: str | None = None
    exists: bool | None = None

class FindBook(BaseModel):
    id: int | None = None
    name: str | None = None
    author: str | None = None
    published_year: int | None = None
    isbn: str | None = None
    amount: int | None = None
    exists: bool | None = None

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