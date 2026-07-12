from fastapi import FastAPI

import models

from database import engine
from routers import vehicles, drivers


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TransitOps API",
    description="Smart Transport Operations Platform",
    version="1.0"
)


app.include_router(vehicles.router)
app.include_router(drivers.router)

@app.get("/")
def home():
    return {
        "message": "TransitOps Backend is Running"
    }