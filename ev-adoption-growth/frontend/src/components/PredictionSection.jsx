import React from 'react';
import ComprehensivePrediction from './ComprehensivePrediction';
import PredictionCard from './PredictionCard';

const PredictionSection = ({ categories, onPredict }) => {
  return (
    <div className="section-view">
      <h2 className="section-title">🔮 Prediction Center</h2>
      <div className="section-grid">
        <ComprehensivePrediction categories={categories} />
        <PredictionCard categories={categories} onPredict={onPredict} />
      </div>
    </div>
  );
};

export default PredictionSection;
