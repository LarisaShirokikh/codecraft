from fastapi import FastAPI

from app.api import user

app = FastAPI(title="Интернет-магазин дверей API")
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API интернет-магазина дверей!"}
