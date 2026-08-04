import React from 'react';

const DashboardHome = ({ top5Growth, co2Data, trendData, setActiveSection }) => {
  const totalEVs = trendData?.total?.[trendData.total.length - 1] || 0;
  const totalCO2 = co2Data?.reduce((sum, item) => sum + item.co2_reduction, 0) || 0;
  const leadCategory = top5Growth?.[0];

  const quickActions = [
    { label: 'Run predictions', detail: 'Generate forward-looking EV demand', target: 'predict' },
    { label: 'Review growth curves', detail: 'Compare segments and yearly trends', target: 'growth' },
    { label: 'Inspect PCS readiness', detail: 'See infrastructure pressure points', target: 'infrastructure' },
    { label: 'Measure climate benefit', detail: 'Track potential CO2 reduction', target: 'environmental' }
  ];

  return (
    <div className="dashboard-home">
      <section className="home-hero-card">
        <div className="home-hero-copy">
          <span className="eyebrow">Mobility command center</span>
          <h2>One place to read EV momentum, future demand, and system readiness.</h2>
          <p>
            Use the dashboard to move from macro adoption signals into practical forecasting,
            charging infrastructure planning, and environmental outcomes.
          </p>
        </div>

        <div className="home-hero-highlight">
          <span className="hero-highlight-label">Strongest projected category</span>
          <strong>{leadCategory?.category || 'Loading trend signals'}</strong>
          <p>
            {leadCategory
              ? `Expected uplift of ${leadCategory.growth.toLocaleString()} registrations by 2035.`
              : 'Growth projections appear here once the trend data is available.'}
          </p>
        </div>
      </section>

      <div className="metrics-grid">
        <div className="metric-card metric-card-primary">
          <div className="metric-value">{totalEVs.toLocaleString()}</div>
          <div className="metric-label">Total EV registrations</div>
        </div>

        <div className="metric-card metric-card-soft">
          <div className="metric-value">{totalCO2.toLocaleString()}</div>
          <div className="metric-label">CO2 reduction potential (tons)</div>
        </div>

        <div className="metric-card metric-card-accent">
          <div className="metric-value">{top5Growth?.length || 0}</div>
          <div className="metric-label">High-growth categories tracked</div>
        </div>

        <div className="metric-card metric-card-outline">
          <div className="metric-value">2035</div>
          <div className="metric-label">Target projection horizon</div>
        </div>
      </div>

      <div className="quick-actions">
        <div className="quick-actions-header">
          <div>
            <span className="eyebrow">Fast paths</span>
            <h3>Jump into the next analysis layer</h3>
          </div>
          <p>Each path keeps the same theme, but shifts the data lens and layout emphasis.</p>
        </div>

        <div className="action-grid">
          {quickActions.map((action) => (
            <button
              key={action.target}
              type="button"
              className="action-card"
              onClick={() => setActiveSection(action.target)}
            >
              <span className="action-index">0{quickActions.indexOf(action) + 1}</span>
              <span className="action-body">
                <span className="action-title">{action.label}</span>
                <span className="action-detail">{action.detail}</span>
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
