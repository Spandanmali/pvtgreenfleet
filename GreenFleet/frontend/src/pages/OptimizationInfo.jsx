export default function OptimizationInfo() {
  return (
    <main className="info-page">
      <div className="info-shell">
        <h1 className="info-title">About optimization</h1>
        <p className="info-copy">
          The recommendation is rule-based rather than an optimization model: it
          checks the submitted weather and fuel type, suggests alternative
          routing in stormy conditions, and suggests switching from HFO to LNG
          or Diesel. When neither condition applies, it says to maintain speed
          and monitor engine telemetry.
        </p>
      </div>
    </main>
  );
}
