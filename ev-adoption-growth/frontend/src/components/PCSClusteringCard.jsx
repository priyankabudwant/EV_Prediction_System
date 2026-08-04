import React from 'react';

const PCSClusteringCard = ({ data }) => {
  if (!data || data.length === 0) return <div className="loader"></div>;

  const clusterColors = {
    0: '#ff6b6b',
    1: '#ffd93d',
    2: '#6bcf7f'
  };

  const clusterNames = {
    0: 'Low Infrastructure',
    1: 'Medium Infrastructure',
    2: 'High Infrastructure'
  };

  return (
    <section className="card">
      <h2 className="card-title">📊 Infrastructure Clusters</h2>
      <div className="stats-container">
        {data.slice(0, 10).map((item, index) => (
          <div 
            key={index} 
            className="stat-item" 
            style={{ 
              animationDelay: `${index * 0.1}s`,
              background: `linear-gradient(135deg, ${clusterColors[item.Cluster]}40 0%, ${clusterColors[item.Cluster]}80 100%)`
            }}
          >
            <div>
              <div className="stat-label">{item.State}</div>
              <div style={{ fontSize: '0.85em', color: '#666' }}>
                {clusterNames[item.Cluster]}
              </div>
            </div>
            <div className="stat-value">{item['No. of Operational PCS'].toLocaleString()} PCS</div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default PCSClusteringCard;
