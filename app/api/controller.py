from fastapi import FastAPI
from app.products.controller import products_router


api = FastAPI()
api.include_router(products_router)
