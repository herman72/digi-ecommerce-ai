
from fastapi import FastAPI
from app.routers.category import router as category_router

app = FastAPI(
    title="digikala agent",
    description="digikala agent",
    version="0.1",
)

app.include_router(category_router, prefix="/category", tags=["goods"])

@app.get("/")
async def root():
    return {"message": "Welcome digikala api!"}





