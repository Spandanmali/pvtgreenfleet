export default function BenchmarkResults() {
  return (
    <main className="info-page">
      <div className="info-shell">
        <h1 className="info-title">Benchmark</h1>
        <img
          className="benchmark-image"
          src="/benchmark_results.png"
          alt="Baseline and XGBoost model performance benchmark"
        />
        <table className="results-table">
          <caption>Model error comparison</caption>
          <tbody>
            <tr>
              <th>Physics MAE</th>
              <td>879.17</td>
            </tr>
            <tr>
              <th>XGBoost MAE</th>
              <td>672.38</td>
            </tr>
            <tr>
              <th>Physics RMSE</th>
              <td>1188.74</td>
            </tr>
            <tr>
              <th>XGBoost RMSE</th>
              <td>1181.69</td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  );
}
