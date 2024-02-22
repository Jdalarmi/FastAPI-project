from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from pydantic import BaseModel, Field
from ..models import Todos
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Todos
from typing import Annotated
from starlette import status
from .auth import get_current_user
from starlette.responses import RedirectResponse

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="Todoapp/templates")


router = APIRouter(
    prefix='/todos-templates',
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request":request})

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    todos = db.query(Todos).filter(Todos.owner == 1).all()
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos})






@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})

@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title:str = Form(...), description:str = Form(...),
                     priority:int = Form(...), db:Session = Depends(get_db)):
    todo_model = Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner = 1

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos-template", status_code=status.HTTP_302_FOUND)



@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

    todo = db.query(Todos).filter(Todos.id == todo.id).first()

    return templates.TemplateResponse("edit-todo.html", {"request":request, "todo":todo})

