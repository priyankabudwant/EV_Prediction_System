import React from 'react';

const Navigation = ({ activeSection, setActiveSection }) => {
  const sections = [
    { id: 'home', tag: '01', label: 'Dashboard', detail: 'Overview and launch points' },
    { id: 'predict', tag: '02', label: 'Predictions', detail: 'Future vehicle demand' },
    { id: 'growth', tag: '03', label: 'Growth Analysis', detail: 'Category and trend signals' },
    { id: 'infrastructure', tag: '04', label: 'Infrastructure', detail: 'PCS readiness and ranking' },
    { id: 'environmental', tag: '05', label: 'Environmental', detail: 'CO2 impact outlook' }
  ];

  return (
    <nav className="navigation">
      {sections.map((section) => (
        <button
          key={section.id}
          className={`nav-item ${activeSection === section.id ? 'active' : ''}`}
          onClick={() => setActiveSection(section.id)}
        >
          <span className="nav-tag">{section.tag}</span>
          <span className="nav-copy">
            <span className="nav-label">{section.label}</span>
            <span className="nav-detail">{section.detail}</span>
          </span>
        </button>
      ))}
    </nav>
  );
};

export default Navigation;
