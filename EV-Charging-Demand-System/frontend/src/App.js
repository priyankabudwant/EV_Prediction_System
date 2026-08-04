import React, { useState } from "react";
import IndiaMap from "./components/IndiaMap";
import ControlPanel from "./components/ControlPanel";
import DemandChart from "./components/DemandChart";

const statsConfig = [
  { key: "High", label: "High Priority Cities" },
  { key: "Medium", label: "Medium Demand Cities" },
  { key: "Low", label: "Low Demand Cities" },
];

export default function App() {
  const [predictions, setPredictions] = useState([]);

  const summary = predictions.reduce(
    (accumulator, city) => {
      const level = city.demand_level || city.level;
      if (accumulator.counts[level] !== undefined) {
        accumulator.counts[level] += 1;
      }

      if (
        !accumulator.topCity ||
        Number(city.score) > Number(accumulator.topCity.score)
      ) {
        accumulator.topCity = city;
      }

      return accumulator;
    },
    {
      counts: { High: 0, Medium: 0, Low: 0 },
      total: predictions.length,
      topCity: null,
    }
  );

  return (
    <main className="app-shell">
      <section className="hero-section">
        <div className="hero-copy">
          <p className="eyebrow">Smart Mobility Intelligence</p>
          <h1>EV Charging Demand Prediction System</h1>
          <p className="hero-text">
            Model charging demand across Indian cities, compare infrastructure
            pressure, and surface where expansion matters most.
          </p>
        </div>

        <div className="hero-highlight panel-surface">
          <span className="hero-badge">Live simulation workspace</span>
          <strong>{summary.total || 0}</strong>
          <p>Cities currently included in the latest demand prediction run.</p>
          <div className="hero-city">
            <span>Top projected city</span>
            <b>{summary.topCity?.city || "Run a prediction"}</b>
          </div>
        </div>
      </section>

      <section className="stats-grid">
        {statsConfig.map((item) => (
          <article key={item.key} className="stat-card panel-surface">
            <span>{item.label}</span>
            <strong>{summary.counts[item.key]}</strong>
          </article>
        ))}
      </section>

      <section className="dashboard-grid">
        <ControlPanel setPredictions={setPredictions} />

        <div className="visual-stack">
          <IndiaMap predictions={predictions} />
          <DemandChart predictions={predictions} />
        </div>
      </section>
    </main>
  );
}
