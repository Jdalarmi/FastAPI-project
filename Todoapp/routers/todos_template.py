from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field
from ..models import Todos
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Todos
from typing import Annotated
from starlette import status
from .auth import get_current_user

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

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse("add-todo.html", {"request": request})



