from fastapi import APIRouter, HTTPException
from app.schemas.fuel import FuelPredictionRequest, FuelPredictionResponse
from app.services.ml_services import ml_service

router = APIRouter()

@router.post("/predict-fuel", response_model=FuelPredictionResponse)
async def predict_fuel(request: FuelPredictionRequest):
    try:
        raw_data = request.dict()
        
        # 1. Get ML Prediction
        ml_prediction = ml_service.predict_ml(raw_data)
        
        # 2. Get Physics Benchmark Estimate
        physics_prediction = ml_service.predict_physics(raw_data)
        
        # 3. Get Optimization Recommendation
        optimization_tip = ml_service.generate_optimization(raw_data, ml_prediction)
        
        return FuelPredictionResponse(
            predicted_fuel_consumption_ml=round(ml_prediction, 2),
            predicted_fuel_consumption_physics=round(physics_prediction, 2),
            optimization_recommendation=optimization_tip
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction and optimization failed: {str(e)}")