from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos
from starlette.staticfiles import StaticFiles

app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.mount("/static", StaticFiles(directory="Todoapp/static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)


