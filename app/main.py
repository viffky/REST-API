from fastapi import FastAPI
from app.api.v1.api import router as api_router
from app.db.base import Base
from app.db.session import engine
from sqlalchemy.ext.asyncio import AsyncEngine

app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Task Management API"}