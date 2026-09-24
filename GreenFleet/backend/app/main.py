from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(
    title="GreenFleet Fuel Prediction & Optimization API",
    version="1.0",
    description="ML-powered maritime fuel consumption and voyage optimization service."
)

# Include our streamlined router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "GreenFleet ML Backend is running successfully!"}