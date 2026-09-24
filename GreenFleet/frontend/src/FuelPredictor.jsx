import { useState } from 'react'

const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

const shipTypes = ['Oil Service Boat', 'Fishing Trawler', 'Surfer Boat', 'Tanker Ship']
const fuelTypes = ['HFO', 'Diesel']
const weatherConditions = ['Calm', 'Moderate', 'Stormy']

const initialForm = {
  distance: '',
  month: 'January',
  route_id: '',
  ship_type: 'Oil Service Boat',
  fuel_type: 'HFO',
  weather_conditions: 'Calm',
  engine_efficiency: '',
}

export default function FuelPredictor() {
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const updateField = (event) => {
    const { name, value } = event.target
    setForm((currentForm) => ({ ...currentForm, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const distance = Number(form.distance)
    const engineEfficiency = Number(form.engine_efficiency)

    if (distance <= 0 || engineEfficiency < 0 || engineEfficiency > 100) {
      setError(true)
      setResult(null)
      return
    }

    setIsSubmitting(true)
    setError(false)

    try {
      const response = await fetch('http://localhost:8000/api/v1/predict-fuel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          distance,
          month: form.month,
          route_id: form.route_id,
          ship_type: form.ship_type,
          fuel_type: form.fuel_type,
          weather_conditions: form.weather_conditions,
          engine_efficiency: engineEfficiency,
        }),
      })

      if (!response.ok) throw new Error('Prediction request failed')
      setResult(await response.json())
    } catch {
      setResult(null)
      setError(true)
    } finally {
      setIsSubmitting(false)
    }
  }

  const fieldStyle = {
    display: 'block',
    width: '100%',
    marginTop: 4,
    padding: 8,
    boxSizing: 'border-box',
  }

  return (
    <main style={{ maxWidth: 560, margin: '0 auto', padding: 24, fontFamily: 'sans-serif' }}>
      <h1>Fuel Predictor</h1>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 14 }}>
        <label>
          Distance (nautical miles)
          <input name="distance" type="number" min="0.01" step="any" required value={form.distance} onChange={updateField} style={fieldStyle} />
        </label>

        <label>
          Month
          <select name="month" value={form.month} onChange={updateField} style={fieldStyle}>
            {months.map((month) => <option key={month} value={month}>{month}</option>)}
          </select>
        </label>

        <label>
          Route ID
          <input name="route_id" type="text" placeholder="Route-A" required value={form.route_id} onChange={updateField} style={fieldStyle} />
        </label>

        <label>
          Ship type
          <select name="ship_type" value={form.ship_type} onChange={updateField} style={fieldStyle}>
            {shipTypes.map((shipType) => <option key={shipType} value={shipType}>{shipType}</option>)}
          </select>
        </label>

        <label>
          Fuel type
          <select name="fuel_type" value={form.fuel_type} onChange={updateField} style={fieldStyle}>
            {fuelTypes.map((fuelType) => <option key={fuelType} value={fuelType}>{fuelType}</option>)}
          </select>
        </label>

        <label>
          Weather conditions
          <select name="weather_conditions" value={form.weather_conditions} onChange={updateField} style={fieldStyle}>
            {weatherConditions.map((weather) => <option key={weather} value={weather}>{weather}</option>)}
          </select>
        </label>

        <label>
          Engine efficiency (0-100)
          <input name="engine_efficiency" type="number" min="0" max="100" step="any" required value={form.engine_efficiency} onChange={updateField} style={fieldStyle} />
        </label>

        <button type="submit" disabled={isSubmitting} style={{ padding: 10 }}>
          {isSubmitting ? 'Predicting...' : 'Predict fuel'}
        </button>
      </form>

      {error && <p role="alert">Error, try again</p>}
      {result && (
        <section aria-live="polite" style={{ marginTop: 24 }}>
          <p>ML Prediction: {result.predicted_fuel_consumption_ml} {result.unit}</p>
          <p>Physics Baseline: {result.predicted_fuel_consumption_physics} {result.unit}</p>
          <p>Recommendation: {result.optimization_recommendation}</p>
        </section>
      )}
    </main>
  )
}
