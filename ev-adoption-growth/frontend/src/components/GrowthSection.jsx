import React from 'react';
import Top5GrowthCard from './Top5GrowthCard';
import ComparisonChart from './ComparisonChart';
import TrendChart from './TrendChart';
import ForecastChart from './ForecastChart';

const GrowthSection = ({ top5Growth, comparisonData, trendData, forecastData }) => {
  return (
    <div className="section-view">
      <h2 className="section-title">📈 Growth Analysis</h2>
      <div className="section-grid">
        <Top5GrowthCard data={top5Growth} />
        <ForecastChart data={forecastData} />
        <ComparisonChart data={comparisonData} />
        <TrendChart data={trendData} />
      </div>
    </div>
  );
};

export default GrowthSection;
