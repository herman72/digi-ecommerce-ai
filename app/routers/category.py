from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.models.db_models import engine, Category
from sqlalchemy.orm import sessionmaker

router = APIRouter()

Session = sessionmaker(bind=engine)
session = Session()
class CategoryQuery(BaseModel):
    category: str

@router.get("/get-category", tags=["Category"])
async def get_category():
    categories = session.query(Category).all()
    return {"categories": [{"id": category.id, "name": category.name} for category in categories]}

