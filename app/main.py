from fastapi import FastAPI
from app.api.routes import router as expense_router




app = FastAPI(title="Trackbablo")
app.include_router(expense_router)

@app.get("/")
def read_root():
    return {"message": "Трекер работает"}

