"""
Train XGBoost fuel prediction model on maritime ship fuel efficiency dataset.
Run: python ml/train.py ml/data/ship_fuel_efficiency.csv
Output: backend/app/ml/fuel_model.joblib
"""

import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import xgboost as xgb
import joblib
from pathlib import Path

def train(data_path: str):
    data_file = Path(data_path)
    if not data_file.exists():
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    print("Preprocessing data...")
    # 1. Sanity Checks
    df = df[(df['distance'] > 0) & (df['fuel_consumption'] > 0) & (df['CO2_emissions'] > 0)]

    # 2. Cyclical Encoding for Month
    month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 
                 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    df['month_num'] = df['month'].map(month_map)
    df['month_sin'] = np.sin(2 * np.pi * df['month_num'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month_num'] / 12)
    df.drop(['month', 'month_num'], axis=1, inplace=True)

    # 3. Target Encoding for route_id
    # Note: For production inference, you will need to save this mapping dictionary
    # to apply the same route averages to new API requests.
    route_target_mean = df.groupby('route_id')['fuel_consumption'].mean()
    df['route_avg_fuel'] = df['route_id'].map(route_target_mean)

    # Save the route mapping for backend inference
    mapping_dir = Path(__file__).parent.parent / "backend" / "app" / "ml"
    mapping_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(route_target_mean.to_dict(), mapping_dir / "route_mapping.joblib")

    # 4. Drop Identifiers
    df.drop(['ship_id', 'route_id'], axis=1, inplace=True)

    # 5. One-Hot Encoding
    df = pd.get_dummies(df, columns=['ship_type', 'fuel_type', 'weather_conditions'], drop_first=True)

    # Save expected feature columns for the FastAPI backend to use during prediction
    expected_features = df.drop(columns=['fuel_consumption', 'CO2_emissions']).columns.tolist()
    joblib.dump(expected_features, mapping_dir / "expected_features.joblib")

    # 6. Separate Features and Target
    X = df.drop(columns=['fuel_consumption', 'CO2_emissions'])
    y = df['fuel_consumption']

    # 7. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
    )
    
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2:   {r2:.4f}")
    print(f"Test MAPE: {mape:.2f}%")

    out_path = mapping_dir / "fuel_model.joblib"
    joblib.dump(model, out_path)
    print(f"Model successfully saved to {out_path}")
    
    return mape

if __name__ == "__main__":
    # Default path assumes running from root directory: python ml/train.py
    default_data_path = "ml/data/ship_fuel_efficiency.csv"
    data_path = sys.argv[1] if len(sys.argv) > 1 else default_data_path
    train(data_path)