from fastapi import FastAPI

import models

from database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TransitOps API",
    description="Smart Transport Operations Platform",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "TransitOps Backend is Running"
    }