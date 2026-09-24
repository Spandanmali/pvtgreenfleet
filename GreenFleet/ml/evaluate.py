"""
Evaluate model performance: Baseline (Linear) vs XGBoost.
Run: python ml/evaluate.py
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path
import sys

def prepare_test_data(data_path: str):
    """Recreates the exact preprocessed test set from train.py"""
    if not Path(data_path).exists():
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)

    df = pd.read_csv(data_path)
    df = df[(df['distance'] > 0) & (df['fuel_consumption'] > 0) & (df['CO2_emissions'] > 0)]

    month_map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 
                 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    df['month_num'] = df['month'].map(month_map)
    df['month_sin'] = np.sin(2 * np.pi * df['month_num'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month_num'] / 12)
    df.drop(['month', 'month_num'], axis=1, inplace=True)

    route_target_mean = df.groupby('route_id')['fuel_consumption'].mean()
    df['route_avg_fuel'] = df['route_id'].map(route_target_mean)
    df.drop(['ship_id', 'route_id'], axis=1, inplace=True)
    df = pd.get_dummies(df, columns=['ship_type', 'fuel_type', 'weather_conditions'], drop_first=True)

    X = df.drop(columns=['fuel_consumption', 'CO2_emissions'])
    y = df['fuel_consumption']

    # Using the exact same random_state guarantees the exact same test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def main():
    data_path = "ml/data/ship_fuel_efficiency.csv"
    model_path = Path(__file__).parent.parent / "backend" / "app" / "ml" / "fuel_model.joblib"
    
    if not model_path.exists():
        print(f"Error: XGBoost model not found at {model_path}. Run train.py first.")
        sys.exit(1)

    print("Preparing data...")
    X_train, X_test, y_train, y_test = prepare_test_data(data_path)

    print("Loading XGBoost model...")
    xgb_model = joblib.load(model_path)
    
    print("Training Baseline (Linear) model...")
    baseline_model = LinearRegression()
    baseline_model.fit(X_train, y_train)

    print("Generating predictions...")
    xgb_preds = xgb_model.predict(X_test)
    base_preds = baseline_model.predict(X_test)

    # Compute Metrics
    xgb_mae = mean_absolute_error(y_test, xgb_preds)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
    
    base_mae = mean_absolute_error(y_test, base_preds)
    base_rmse = np.sqrt(mean_squared_error(y_test, base_preds))

    # Print Comparison Table
    print("\n" + "="*50)
    print(f"{'Metric':<15} | {'Baseline (Linear)':<20} | {'XGBoost':<10}")
    print("-" * 50)
    print(f"{'MAE':<15} | {base_mae:<20.2f} | {xgb_mae:<10.2f}")
    print(f"{'RMSE':<15} | {base_rmse:<20.2f} | {xgb_rmse:<10.2f}")
    print("="*50 + "\n")

    # Plot Bar Chart
    labels = ['MAE', 'RMSE']
    base_scores = [base_mae, base_rmse]
    xgb_scores = [xgb_mae, xgb_rmse]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x - width/2, base_scores, width, label='Baseline (Linear)', color='lightgray')
    ax.bar(x + width/2, xgb_scores, width, label='XGBoost', color='teal')

    ax.set_ylabel('Error (Lower is Better)')
    ax.set_title('Model Performance Benchmark: Baseline vs XGBoost')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plot_path = "ml/benchmark_results.png"
    plt.savefig(plot_path)
    print(f"Chart saved to {plot_path}")
    plt.show()

if __name__ == "__main__":
    main()