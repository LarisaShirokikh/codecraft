from fastapi import FastAPI
from app.config import settings

app = FastAPI(title="CodeCraft", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to CodeCraft!"}