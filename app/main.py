from fastapi import FastAPI
from app.api.controller import api

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/api", api)
