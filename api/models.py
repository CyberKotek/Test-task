from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import schemas
from datetime import datetime, timezone

class Readers(Base):
    __tablename__ = "readers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    borrows = relationship("Borrows", back_populates="reader")
    returned_borrows = relationship("ReturnedBorrows", back_populates="reader")


    def __init__(self, reader: schemas.Reader):
        self.name = reader.name
        self.email = reader.email


class Librarians(Base):
    __tablename__ = "librarians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # def __init__(self, librarian: schemas.Librarian):
    #     self.email = librarian.email
    #     self.name = librarian.name
    #     self.password = librarian.password


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    amount = Column(Integer, default=1)

    borrows = relationship("Borrows", back_populates="book")
    returned_borrows = relationship("ReturnedBorrows", back_populates="book")

    def __init__(self, book: schemas.Book):
        self.name = book.name
        self.author = book.author
        self.published_year = book.published_year
        self.isbn = book.isbn
        self.amount = book.amount


class Borrows(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(DateTime, nullable=False)

    book = relationship("Books", back_populates="borrows")
    reader = relationship("Readers", back_populates="borrows")
    
    def __init__(self, borrow: schemas.Borrow):
        self.book_id = borrow.book_id
        self.reader_id = borrow.reader_id
        if (not borrow.borrow_date):
            self.borrow_date = datetime.now(timezone.utc)
        else:
            self.borrow_date = borrow.borrow_date


class ReturnedBorrows(Base):
    __tablename__ = "returned_borrows"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)

    book = relationship("Books", back_populates="returned_borrows")
    reader = relationship("Readers", back_populates="returned_borrows")

    def __init__(self, borrow: Borrows):
        self.book_id = borrow.book_id
        self.reader_id = borrow.reader_id
        if (not borrow.borrow_date):
            self.borrow_date = datetime.now(timezone.utc)
        else:
            self.borrow_date = borrow.borrow_date

        self.return_date = datetime.now(timezone.utc)
