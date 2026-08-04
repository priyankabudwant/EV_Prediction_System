import React from 'react';
import PCSClusteringCard from './PCSClusteringCard';
import PCSProjectionCard from './PCSProjectionCard';
import PCSRankingCard from './PCSRankingCard';

const InfrastructureSection = ({ pcsClustering, pcsProjection, pcsRanking }) => {
  return (
    <div className="section-view">
      <h2 className="section-title">🔌 Infrastructure Analysis</h2>
      <div className="section-grid">
        <PCSClusteringCard data={pcsClustering} />
        <PCSProjectionCard data={pcsProjection} />
        <PCSRankingCard data={pcsRanking} />
      </div>
    </div>
  );
};

export default InfrastructureSection;
