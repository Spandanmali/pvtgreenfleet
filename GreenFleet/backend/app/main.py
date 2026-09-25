from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(
    title="GreenFleet Fuel Prediction & Optimization API",
    version="1.0",
    description="ML-powered maritime fuel consumption and voyage optimization service."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our streamlined router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "GreenFleet ML Backend is running successfully!"}