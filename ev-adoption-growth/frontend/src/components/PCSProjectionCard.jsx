import React from 'react';

const PCSProjectionCard = ({ data }) => {
  if (!data || data.length === 0) return <div className="loader"></div>;

  return (
    <section className="card">
      <h2 className="card-title">🔮 PCS Projection (5 Years)</h2>
      <div className="stats-container">
        {data.map((item, index) => (
          <div key={index} className="stat-item" style={{ animationDelay: `${index * 0.1}s` }}>
            <div>
              <div className="stat-label">{item.State}</div>
              <div style={{ fontSize: '0.85em', color: '#666' }}>
                Current: {item['No. of Operational PCS'].toLocaleString()} PCS
              </div>
            </div>
            <div className="stat-value">{Math.round(item.Projected_PCS_5Y).toLocaleString()}</div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default PCSProjectionCard;
