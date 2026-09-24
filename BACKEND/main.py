from fastapi import FastAPI
from database import engine
from router import router
import models 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CRUD de Produtos",
    description="CRUD de produtos com FastAPI, PostgreSQL e Docker",
    version="1.0.0",
)

app.include_router(router)