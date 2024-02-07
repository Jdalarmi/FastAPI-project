from fastapi import FastAPI, Body
from pydantic import BaseModel


app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description =description
        self.rating=rating

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


BOOKS = [
    Book(1, 'Computer Science', 'codwithroby', "A very nice book", 5),
    Book(2, 'Be Fast With fastapi', 'codwithroby', "A great book", 2),
    Book(3, 'Master Endpoints', 'codwithroby', "Awesome book", 3),
    Book(4, 'HP1', 'Author 1', "Book description", 4),
    Book(5, 'HP2', 'Author 2', "Book description", 5),
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post(("/create_book"))
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)