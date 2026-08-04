import React, { useState } from 'react';

const ComprehensivePrediction = ({ categories }) => {
  const [category, setCategory] = useState('');
  const [year, setYear] = useState(2030);
  const [state, setState] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!category || !year) {
      alert('Please select category and year');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/comprehensive-predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, year: parseInt(year), state })
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Prediction failed');
    }
    setLoading(false);
  };

  return (
    <section className="card comprehensive-card">
      <h2 className="card-title">🎯 Comprehensive EV Prediction System</h2>
      
      <div className="prediction-form">
        <div className="form-row">
          <div className="form-group">
            <label>Vehicle Category:</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)} className="input-field">
              <option value="">Select Category...</option>
              {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
            </select>
          </div>

          <div className="form-group">
            <label>Prediction Year:</label>
            <input 
              type="number" 
              value={year} 
              onChange={(e) => setYear(e.target.value)} 
              className="input-field" 
              min="2025" 
              max="2050" 
            />
          </div>

          <div className="form-group">
            <label>State (Optional):</label>
            <input 
              type="text" 
              value={state} 
              onChange={(e) => setState(e.target.value)} 
              className="input-field" 
              placeholder="e.g., Maharashtra"
            />
          </div>
        </div>

        <button onClick={handlePredict} className="btn btn-primary" disabled={loading}>
          {loading ? 'Predicting...' : 'Generate Complete Prediction'}
        </button>
      </div>

      {results && (
        <div className="prediction-results">
          <div className="result-grid">
            <div className="result-card">
              <h3>📊 Vehicle Registrations</h3>
              <div className="result-value">{results.vehicle_prediction?.toLocaleString()}</div>
              <div className="result-label">Predicted vehicles in {year}</div>
            </div>

            <div className="result-card">
              <h3>📈 Growth Rate</h3>
              <div className="result-value">{results.growth_rate}%</div>
              <div className="result-label">Annual growth rate</div>
            </div>

            <div className="result-card">
              <h3>🌱 CO2 Reduction</h3>
              <div className="result-value">{results.co2_reduction?.toLocaleString()}</div>
              <div className="result-label">Tons CO₂ saved annually</div>
            </div>

            <div className="result-card">
              <h3>🔌 Required PCS</h3>
              <div className="result-value">{results.required_pcs?.toLocaleString()}</div>
              <div className="result-label">Charging stations needed</div>
            </div>

            <div className="result-card">
              <h3>💰 Market Value</h3>
              <div className="result-value">₹{results.market_value?.toLocaleString()}</div>
              <div className="result-label">Estimated market size (Cr)</div>
            </div>

            <div className="result-card">
              <h3>⚡ Energy Demand</h3>
              <div className="result-value">{results.energy_demand?.toLocaleString()}</div>
              <div className="result-label">MWh required annually</div>
            </div>
          </div>

          {results.insights && (
            <div className="insights-section">
              <h3>💡 Key Insights</h3>
              <ul className="insights-list">
                {results.insights.map((insight, idx) => (
                  <li key={idx}>{insight}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default ComprehensivePrediction;
