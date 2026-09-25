import { useState } from "react";

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const shipTypes = [
  "Oil Service Boat",
  "Fishing Trawler",
  "Surfer Boat",
  "Tanker Ship",
];
const fuelTypes = ["HFO", "Diesel"];
const weatherConditions = ["Calm", "Moderate", "Stormy"];

const initialForm = {
  distance: "",
  month: "January",
  route_id: "",
  ship_type: "Oil Service Boat",
  fuel_type: "HFO",
  weather_conditions: "Calm",
  engine_efficiency: "",
};

export default function FuelPredictor() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const updateField = (event) => {
    const { name, value } = event.target;
    setForm((currentForm) => ({ ...currentForm, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const distance = Number(form.distance);
    const engineEfficiency = Number(form.engine_efficiency);

    if (distance <= 0 || engineEfficiency < 0 || engineEfficiency > 100) {
      setError(true);
      setResult(null);
      return;
    }

    setIsSubmitting(true);
    setError(false);

    try {
      const response = await fetch(
        "https://pvtgreenfleet-production.up.railway.app/api/v1/predict-fuel",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            distance,
            month: form.month,
            route_id: form.route_id,
            ship_type: form.ship_type,
            fuel_type: form.fuel_type,
            weather_conditions: form.weather_conditions,
            engine_efficiency: engineEfficiency,
          }),
        },
      );

      if (!response.ok) throw new Error("Prediction request failed");
      setResult(await response.json());
    } catch {
      setResult(null);
      setError(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="predictor-page">
      <div className="predictor-shell">
        <h1 className="predictor-title">Predict</h1>
        <form className="predictor-form" onSubmit={handleSubmit}>
          <label className="predictor-field">
            <span className="predictor-label">Distance (nautical miles)</span>
            <input
              name="distance"
              type="number"
              min="0.01"
              step="any"
              required
              value={form.distance}
              onChange={updateField}
            />
          </label>

          <label className="predictor-field">
            <span className="predictor-label">Month</span>
            <select name="month" value={form.month} onChange={updateField}>
              {months.map((month) => (
                <option key={month} value={month}>
                  {month}
                </option>
              ))}
            </select>
          </label>

          <label className="predictor-field">
            <span className="predictor-label">Route ID</span>
            <select
              name="route_id"
              required
              value={form.route_id}
              onChange={updateField}
            >
              <option value="Warri-Bonny">Warri-Bonny</option>
              <option value="Port Harcourt-Lagos">Port Harcourt-Lagos</option>
              <option value="Lagos-Apapa">Lagos-Apapa</option>
              <option value="Escravos-Lagos">Escravos-Lagos</option>
            </select>
          </label>

          <label className="predictor-field">
            <span className="predictor-label">Ship type</span>
            <select
              name="ship_type"
              value={form.ship_type}
              onChange={updateField}
            >
              {shipTypes.map((shipType) => (
                <option key={shipType} value={shipType}>
                  {shipType}
                </option>
              ))}
            </select>
          </label>

          <label className="predictor-field">
            <span className="predictor-label">Fuel type</span>
            <select
              name="fuel_type"
              value={form.fuel_type}
              onChange={updateField}
            >
              {fuelTypes.map((fuelType) => (
                <option key={fuelType} value={fuelType}>
                  {fuelType}
                </option>
              ))}
            </select>
          </label>

          <label className="predictor-field">
            <span className="predictor-label">Weather conditions</span>
            <select
              name="weather_conditions"
              value={form.weather_conditions}
              onChange={updateField}
            >
              {weatherConditions.map((weather) => (
                <option key={weather} value={weather}>
                  {weather}
                </option>
              ))}
            </select>
          </label>

          <label className="predictor-field">
            <span className="predictor-label">Engine efficiency (0-100)</span>
            <input
              name="engine_efficiency"
              type="number"
              min="0"
              max="100"
              step="any"
              required
              value={form.engine_efficiency}
              onChange={updateField}
            />
          </label>

          <button
            className="predictor-submit"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Predicting..." : "Predict fuel"}
          </button>
        </form>

        {error && (
          <p className="predictor-error" role="alert">
            Error, try again
          </p>
        )}
        {result && (
          <section className="predictor-results" aria-live="polite">
            <div className="predictor-result-row predictor-result-primary">
              <span>ML Prediction</span>
              <strong>
                {result.predicted_fuel_consumption_ml} {result.unit}
              </strong>
            </div>
            <div className="predictor-result-row">
              <span>Physics Baseline</span>
              <strong>
                {result.predicted_fuel_consumption_physics} {result.unit}
              </strong>
            </div>
            <p className="predictor-recommendation">
              <span>Recommendation</span>
              {result.optimization_recommendation}
            </p>
          </section>
        )}
      </div>
    </main>
  );
}
