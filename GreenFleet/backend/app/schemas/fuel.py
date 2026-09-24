from pydantic import BaseModel, Field

class FuelPredictionRequest(BaseModel):
    distance: float = Field(..., gt=0, description="Distance travelled in nautical miles")
    month: str = Field(..., description="Month of the voyage (e.g., 'January')")
    route_id: str = Field(..., description="Route identifier (e.g., 'Warri-Bonny')")
    ship_type: str = Field(..., description="Type of vessel (e.g., 'Oil Service Boat')")
    fuel_type: str = Field(..., description="Type of fuel used (e.g., 'HFO', 'Diesel')")
    weather_conditions: str = Field(..., description="Weather during voyage (e.g., 'Calm', 'Moderate', 'Stormy')")
    engine_efficiency: float = Field(..., gt=0, le=100, description="Engine efficiency percentage")

class FuelPredictionResponse(BaseModel):
    predicted_fuel_consumption_ml: float
    predicted_fuel_consumption_physics: float
    optimization_recommendation: str
    unit: str = "metric tons"