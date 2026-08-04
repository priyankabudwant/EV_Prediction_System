import React from 'react';
import CO2ReductionCard from './CO2ReductionCard';

const EnvironmentalSection = ({ co2Data }) => {
  const totalCO2 = co2Data?.reduce((sum, item) => sum + item.co2_reduction, 0) || 0;

  return (
    <div className="section-view">
      <h2 className="section-title">🌱 Environmental Impact</h2>
      <div className="environmental-overview">
        <div className="impact-card">
          <h3>Total CO₂ Reduction by 2035</h3>
          <div className="impact-value">{totalCO2.toLocaleString()} tons</div>
          <p>Equivalent to planting {Math.round(totalCO2 * 50).toLocaleString()} trees</p>
        </div>
      </div>
      <div className="section-grid">
        <CO2ReductionCard data={co2Data} />
      </div>
    </div>
  );
};

export default EnvironmentalSection;
