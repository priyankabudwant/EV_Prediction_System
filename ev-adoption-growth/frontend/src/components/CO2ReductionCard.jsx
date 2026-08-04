import React from 'react';

const CO2ReductionCard = ({ data }) => {
  if (!data || data.length === 0) return <div className="loader"></div>;

  return (
    <section className="card">
      <h2 className="card-title">🌱 CO2 Reduction Impact (2035)</h2>
      <div className="stats-container">
        {data.map((item, index) => (
          <div key={index} className="stat-item co2-item" style={{ animationDelay: `${index * 0.1}s` }}>
            <div className="stat-label">{item.category}</div>
            <div className="stat-value">{item.co2_reduction.toLocaleString()} tons CO₂</div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default CO2ReductionCard;
