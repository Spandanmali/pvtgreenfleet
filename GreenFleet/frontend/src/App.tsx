import FuelPredictor from './FuelPredictor'
import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import BenchmarkResults from './pages/BenchmarkResults'
import OptimizationInfo from './pages/OptimizationInfo'

export default function App() {
  return (
    <BrowserRouter>
      <nav className="top-nav" aria-label="Main navigation">
        <NavLink to="/" end>Predict</NavLink>
        <NavLink to="/benchmark">Benchmark</NavLink>
        <NavLink to="/about">About</NavLink>
      </nav>
      <Routes>
        <Route path="/" element={<FuelPredictor />} />
        <Route path="/benchmark" element={<BenchmarkResults />} />
        <Route path="/about" element={<OptimizationInfo />} />
      </Routes>
    </BrowserRouter>
  )
}
