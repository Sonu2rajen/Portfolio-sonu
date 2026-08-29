from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.database import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return {"message": "Resume Parser API is running"}
