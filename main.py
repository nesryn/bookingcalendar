
from fastapi import FastAPI
from database import Base, engine
import models
from routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Salon Booking API",
    description="Backend API for the Salon Booking",
    version="0.1.0",
)

app.include_router(auth.router)