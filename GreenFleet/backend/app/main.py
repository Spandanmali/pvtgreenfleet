from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router

app = FastAPI(
    title="GreenFleet Fuel Prediction & Optimization API",
    version="1.0",
    description="ML-powered maritime fuel consumption and voyage optimization service."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pvtgreenfleet-one.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "GreenFleet ML Backend is running successfully!"}