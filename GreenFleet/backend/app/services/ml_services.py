import pandas as pd
import numpy as np
import joblib
from pathlib import Path

class FuelPredictionService:
    def __init__(self):
        base_dir = Path(__file__).parent.parent / "ml"
        
        # Load artifacts
        self.model = joblib.load(base_dir / "fuel_model.joblib")
        self.route_mapping = joblib.load(base_dir / "route_mapping.joblib")
        self.expected_features = joblib.load(base_dir / "expected_features.joblib")
        
        self.month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 
            'May': 5, 'June': 6, 'July': 7, 'August': 8, 
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }

    def preprocess_input(self, raw_data: dict) -> pd.DataFrame:
        df = pd.DataFrame([raw_data])
        month_num = self.month_map.get(df['month'].iloc[0], 1)
        df['month_sin'] = np.sin(2 * np.pi * month_num / 12)
        df['month_cos'] = np.cos(2 * np.pi * month_num / 12)
        df.drop(columns=['month'], inplace=True)
        
        global_route_mean = sum(self.route_mapping.values()) / len(self.route_mapping) if self.route_mapping else 0
        df['route_avg_fuel'] = df['route_id'].map(self.route_mapping).fillna(global_route_mean)
        df.drop(columns=['route_id'], inplace=True)
        
        df = pd.get_dummies(df, columns=['ship_type', 'fuel_type', 'weather_conditions'])
        
        for col in self.expected_features:
            if col not in df.columns:
                df[col] = 0
                
        return df[self.expected_features]

    def predict_ml(self, raw_data: dict) -> float:
        processed_df = self.preprocess_input(raw_data)
        prediction = self.model.predict(processed_df)
        return float(prediction[0])

    def predict_physics(self, raw_data: dict) -> float:
        """Legacy physics benchmark formula calculation."""
        distance = raw_data.get("distance", 100)
        efficiency = raw_data.get("engine_efficiency", 85)
        # Base linear/proportional estimate adjusted by engine efficiency coefficient
        base_estimate = (distance * 35.0) * (90.0 / max(efficiency, 50.0))
        return float(base_estimate)

    def generate_optimization(self, raw_data: dict, ml_pred: float) -> str:
        """Generates real-time optimization advice for the dashboard demo."""
        weather = raw_data.get("weather_conditions", "Calm")
        fuel_type = raw_data.get("fuel_type", "HFO")
        
        tips = []
        if weather == "Stormy":
            tips.append("Adverse weather detected: Consider alternative routing to avoid heavy seas and reduce resistance.")
        if fuel_type == "HFO":
            tips.append("Switching from Heavy Fuel Oil (HFO) to LNG or Diesel can cut local particulate emissions and optimize profile.")
        
        if not tips:
            tips.append("Voyage parameters are optimal. Maintain current cruising speed and monitor engine telemetry.")
            
        return " | ".join(tips)

ml_service = FuelPredictionService()