from fastapi import FastAPI
from database import engine
from router import router
import models 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)