import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div className="header-copy">
        <span className="eyebrow">Action plan</span>
        <h1 className="title">EV Pulse Control Room</h1>
        <p className="subtitle">Distinct view, same EV theme, sharper hierarchy for forecasting adoption, infrastructure load, and environmental impact.</p>
      </div>

      <div className="header-aside">
        <div className="header-stat">
          <span>Theme</span>
          <strong>Neon EV command</strong>
        </div>
        <div className="header-stat">
          <span>Layout</span>
          <strong>Responsive control room</strong>
        </div>
      </div>
    </header>
  );
};

export default Header;
