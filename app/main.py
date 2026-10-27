from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router as expense_router
from app.core.config import settings
from app.database.db import Base, engine
from app.models.expense import Expense

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI( title=settings.app_name, lifespan=lifespan, )

app.include_router(expense_router)

@app.get("/")
def read_root():
    return {"message": "Трекер работает"}


