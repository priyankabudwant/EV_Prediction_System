import React, { useState } from "react";
import { predictDemand } from "../Services/api";

export default function ControlPanel({ setPredictions }) {
  const [chargers, setChargers] = useState(50);
  const [fastRatio, setFastRatio] = useState(40);
  const [sessions, setSessions] = useState(100);
  const [occupancy, setOccupancy] = useState(60);
  const [evGrowth, setEvGrowth] = useState(12);
  const [population, setPopulation] = useState(15000);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    setLoading(true);
    setError("");

    try {
      const result = await predictDemand({
        charger_count: Number(chargers),
        fast_ratio: Number(fastRatio) / 100,
        avg_sessions: Number(sessions),
        occupancy: Number(occupancy) / 100,
        ev_growth: Number(evGrowth) / 100,
        population_density: Number(population),
      });

      setPredictions(result.cities || []);
    } catch (requestError) {
      setError(requestError.message || "Unable to fetch predictions.");
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <aside className="panel-surface control-panel">
      <div className="panel-heading">
        <p className="eyebrow">Simulation Inputs</p>
        <h2>Scenario Designer</h2>
        <p className="section-copy">
          Adjust station capacity and adoption assumptions, then generate a
          fresh demand distribution snapshot.
        </p>
      </div>

      <div className="form-grid">
        <div className="input-group">
          <label htmlFor="charger-count">Charger Count</label>
          <input
            id="charger-count"
            type="number"
            min="1"
            value={chargers}
            onChange={(e) => setChargers(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label htmlFor="fast-ratio">Fast Charger Ratio (%)</label>
          <input
            id="fast-ratio"
            type="number"
            min="0"
            max="100"
            value={fastRatio}
            onChange={(e) => setFastRatio(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label htmlFor="daily-sessions">Avg Daily Sessions</label>
          <input
            id="daily-sessions"
            type="number"
            min="1"
            value={sessions}
            onChange={(e) => setSessions(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label htmlFor="occupancy">Occupancy (%)</label>
          <input
            id="occupancy"
            type="number"
            min="0"
            max="100"
            value={occupancy}
            onChange={(e) => setOccupancy(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label htmlFor="ev-growth">EV Growth (%)</label>
          <input
            id="ev-growth"
            type="number"
            min="0"
            max="100"
            value={evGrowth}
            onChange={(e) => setEvGrowth(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label htmlFor="population-density">Population Density</label>
          <input
            id="population-density"
            type="number"
            min="0"
            value={population}
            onChange={(e) => setPopulation(e.target.value)}
          />
        </div>
      </div>

      {error ? <p className="error-text">{error}</p> : null}

      <button className="primary-button" onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict Demand"}
      </button>
    </aside>
  );
}
