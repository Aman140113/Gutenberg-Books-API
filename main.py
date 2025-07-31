from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship, selectinload, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, select, and_, or_, func
from typing import List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from dotenv import load_dotenv
import os
import ssl

load_dotenv()  # must come BEFORE you access os.getenv

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment")

ssl_context = ssl.create_default_context()

from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"ssl": ssl_context}
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# new changes 

from sqlalchemy import Table, MetaData

metadata = Base.metadata

books_book_authors = Table(
    "books_book_authors",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", ForeignKey("books_book.id")),
    Column("author_id", ForeignKey("books_author.id")),
)

books_book_bookshelves = Table(
    "books_book_bookshelves",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", ForeignKey("books_book.id")),
    Column("bookshelf_id", ForeignKey("books_bookshelf.id")),
)

books_book_subjects = Table(
    "books_book_subjects",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", ForeignKey("books_book.id")),
    Column("subject_id", ForeignKey("books_subject.id")),
)

books_book_languages = Table(
    "books_book_languages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("book_id", ForeignKey("books_book.id")),
    Column("language_id", ForeignKey("books_language.id")),
)

# SQLAlchemy Models


class Book(Base):
    __tablename__ = "books_book"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    download_count = Column(Integer)

    formats = relationship("Format", back_populates="book")
    authors = relationship("Author", secondary=books_book_authors, back_populates="books")
    subjects = relationship("Subject", secondary=books_book_subjects, back_populates="books")
    bookshelves = relationship("Bookshelf", secondary=books_book_bookshelves, back_populates="books")
    languages = relationship("Language", secondary=books_book_languages, back_populates="books")

class Author(Base):
    __tablename__ = "books_author"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=books_book_authors, back_populates="authors")

class Bookshelf(Base):
    __tablename__ = "books_bookshelf"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=books_book_bookshelves, back_populates="bookshelves")

class Subject(Base):
    __tablename__ = "books_subject"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=books_book_subjects, back_populates="subjects")

class Language(Base):
    __tablename__ = "books_language"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    books = relationship("Book", secondary=books_book_languages, back_populates="languages")

class Format(Base):
    __tablename__ = "books_format"
    id = Column(Integer, primary_key=True)
    mime_type = Column(String)
    url = Column(String)
    book_id = Column(Integer, ForeignKey("books_book.id"))
    book = relationship("Book", back_populates="formats")

# Pydantic Schemas
class FormatOut(BaseModel):
    mime_type: str
    url: str
    class Config:
        orm_mode = True

class BookOut(BaseModel):
    title: Optional[str]
    download_count: Optional[int]
    authors: List[str] = []
    languages: List[str] = []
    subjects: List[str] = []
    bookshelves: List[str] = []
    formats: List[FormatOut] = []
    class Config:
        orm_mode = True


class PaginatedBooks(BaseModel):
    total: int
    books: List[BookOut]

# FastAPI App
app = FastAPI()

@app.get("/books", response_model=PaginatedBooks)
async def get_books(
    session: AsyncSession = Depends(get_session),
    book_id: Optional[List[int]] = Query(None),
    language: Optional[List[str]] = Query(None),
    mime_type: Optional[List[str]] = Query(None),
    topic: Optional[List[str]] = Query(None),
    author: Optional[str] = None,
    title: Optional[str] = None,
    offset: int = 0,
    limit: int = 25
):
    stmt = select(Book).options(
        selectinload(Book.authors),
        selectinload(Book.subjects),
        selectinload(Book.bookshelves),
        selectinload(Book.formats),
        selectinload(Book.languages)
    )

    if book_id:
        stmt = stmt.where(Book.id.in_(book_id))

    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))

    if author:
        stmt = stmt.join(Book.authors).where(Author.name.ilike(f"%{author}%"))

    if topic:
        topic_filters = []
        for t in topic:
            topic_filters.append(Subject.name.ilike(f"%{t}%"))
            topic_filters.append(Bookshelf.name.ilike(f"%{t}%"))
        stmt = stmt.join(Book.subjects).join(Book.bookshelves).where(or_(*topic_filters))

    if language:
        stmt = stmt.join(Book.languages).where(Language.code.in_(language))

    if mime_type:
        stmt = stmt.join(Book.formats).where(Format.mime_type.in_(mime_type))

    total_count = await session.execute(stmt)
    total = len(total_count.scalars().all())

    stmt = stmt.order_by(Book.download_count.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    books = result.scalars().all()

    books_out = []
    for b in books:
        books_out.append(BookOut(
            title=b.title,
            download_count=b.download_count,
            authors=[a.name for a in b.authors],
            languages=[l.code for l in b.languages],
            subjects=[s.name for s in b.subjects],
            bookshelves=[bs.name for bs in b.bookshelves],
            formats=[FormatOut(mime_type=f.mime_type, url=f.url) for f in b.formats]
        ))

    return {"total": total, "books": books_out}
