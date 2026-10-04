from config import INDEX_NAME_DEFAULT
from utils import get_es_client

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import searchRoute

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status":"ok"}


app.include_router(searchRoute.router)