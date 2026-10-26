from fastapi import FastAPI


app = FastAPI(title="Trackbablo")


@app.get("/")
def read_root():
    return {"message": "Трекер работает"}

