from fastapi import FastAPI
import models
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todos


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

