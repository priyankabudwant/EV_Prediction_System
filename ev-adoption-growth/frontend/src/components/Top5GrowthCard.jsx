import React from 'react';

const Top5GrowthCard = ({ data }) => {
  if (!data || data.length === 0) return <div className="loader"></div>;

  return (
    <section className="card">
      <h2 className="card-title">🚀 Top 5 Growing Categories (2035)</h2>
      <div className="stats-container">
        {data.map((item, index) => (
          <div key={index} className="stat-item" style={{ animationDelay: `${index * 0.1}s` }}>
            <div>
              <div className="stat-label">{item.category}</div>
              <div style={{ fontSize: '0.9em', color: '#666' }}>
                Current: {item.current.toLocaleString()} → 2035: {item.future.toLocaleString()}
              </div>
            </div>
            <div className="stat-value">+{item.growth.toLocaleString()}</div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Top5GrowthCard;
