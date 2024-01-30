from pydantic import BaseModel
from fastapi import FastAPI

fastapi = FastAPI()
class Item(BaseModel):
    name: str
    price: float

@fastapi.post("/items")
async def create_item(item: Item):
    return {"item": item}