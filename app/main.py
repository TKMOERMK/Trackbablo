from fastapi import FastAPI
from app.api.routes import router as expense_router
from app.core.config import settings



app = FastAPI(title=settings.app_name)
app.include_router(expense_router)

@app.get("/")
def read_root():
    return {"message": "Трекер работает"}

