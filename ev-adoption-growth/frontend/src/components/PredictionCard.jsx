import React, { useState } from 'react';

const PredictionCard = ({ categories, onPredict }) => {
  const [selectedCategory, setSelectedCategory] = useState('');
  const [year, setYear] = useState(2030);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  const handlePredict = async () => {

    // ✅ Validation check
    if (!selectedCategory) {
      setError("Please select anything");
      setPrediction(null);
      return; // 🚨 stop function here
    }

    setError(""); // clear old error

    try {
      const result = await onPredict(selectedCategory, year);
      setPrediction(result);
    } catch (err) {
      setError("Something went wrong");
    }
  };

  return (
    <section className="card">
      <h2 className="card-title">🔮 Future Prediction</h2>

      <div className="form-group">
        <label>Select Category:</label>
        <select 
          value={selectedCategory} 
          onChange={(e) => setSelectedCategory(e.target.value)} 
          className="input-field"
        >
          <option value="">Select...</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Select Year:</label>
        <input 
          type="number" 
          value={year} 
          onChange={(e) => setYear(e.target.value)} 
          className="input-field" 
          min="2025" 
          max="2050" 
        />
      </div>

      <button onClick={handlePredict} className="btn btn-primary">
        Predict
      </button>

      {/* ✅ Show error message */}
      {error && (
        <div style={{ color: "red", marginTop: "10px" }}>
          {error}
        </div>
      )}

      {/* ✅ Show prediction result */}
      {prediction && (
        <div className="result-box success-message">
          <strong>{prediction.category}</strong><br />
          Predicted registrations in {prediction.year}: <br />
          <span style={{ fontSize: '1.5em' }}>
            {prediction.prediction.toLocaleString()}
          </span> vehicles
        </div>
      )}
    </section>
  );
};

export default PredictionCard;
