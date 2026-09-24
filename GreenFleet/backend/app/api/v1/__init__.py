from fastapi import APIRouter
from app.api.v1 import predict

api_router = APIRouter()

# Include only the core prediction and optimization router
api_router.include_router(predict.router, prefix="", tags=["Predictions"])