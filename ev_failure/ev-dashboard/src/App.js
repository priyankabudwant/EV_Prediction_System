import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";
import "./App.css";

const tabs = [
  { id: "dashboard", label: "Dashboard", kicker: "Live fleet status" },
  { id: "analytics", label: "Analytics", kicker: "Predictive signals" },
  { id: "vehicle", label: "Vehicle", kicker: "Deep diagnostics" },
  { id: "maintenance", label: "Maintenance", kicker: "Action plan" },
];

const formatPercent = (value = 0, digits = 0) => `${Number(value).toFixed(digits)}%`;
const formatCurrency = (value = 0) => `INR ${Number(value).toLocaleString()}`;

function App() {
  const [fleet, setFleet] = useState([]);
  const [topVehicle, setTopVehicle] = useState(null);
  const [health, setHealth] = useState(100);
  const [history, setHistory] = useState([]);
  const [shapData, setShapData] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [error, setError] = useState("");

  const fetchAll = async () => {
    try {
      setError("");
      const [fleetRes, topRes, healthRes, historyRes, shapRes, analysisRes] =
        await Promise.all([
          axios.get("http://127.0.0.1:8003/fleet"),
          axios.get("http://127.0.0.1:8003/top-vehicle"),
          axios.get("http://127.0.0.1:8003/fleet-health"),
          axios.get("http://127.0.0.1:8003/vehicle-history"),
          axios.get("http://127.0.0.1:8003/shap-analysis"),
          axios.get("http://127.0.0.1:8003/vehicle-analysis"),
        ]);

      setFleet(fleetRes.data);
      setTopVehicle(topRes.data);
      setHealth(healthRes.data.health_score);
      setHistory(historyRes.data);
      setShapData(
        Object.entries(shapRes.data.features).map(([key, value]) => ({
          name: key.replace(/_/g, " "),
          value: Math.abs(value),
        }))
      );
      setAnalysis(analysisRes.data);
    } catch (fetchError) {
      console.error("Error:", fetchError);
      setError("Unable to reach the EV analytics API.");
    }
  };

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!analysis) {
    return (
      <div className="loading-shell">
        <div className="loading-panel">
          <span className="eyebrow">EV Predictive Maintenance</span>
          <h1>Loading dashboard</h1>
          <p>Connecting to live fleet telemetry and diagnostics.</p>
          {error ? <div className="status-banner error">{error}</div> : null}
        </div>
      </div>
    );
  }

  const activeTabData = tabs.find((tab) => tab.id === activeTab);
  const failureRisk = Number((analysis.failure_probability || 0) * 100);
  const liveRiskAvg = fleet.length
    ? fleet.reduce((sum, vehicle) => sum + vehicle.probability, 0) / fleet.length
    : 0;

  const historyTimeline = history.slice(-8).map((item, index) => ({
    name: `T${index + 1}`,
    probability: Number(((item.probability || 0) * 100).toFixed(1)),
  }));

  const signalCards = [
    {
      label: "Fleet health",
      value: formatPercent(health),
      meta: "Overall operating readiness",
    },
    {
      label: "Peak risk",
      value: topVehicle ? formatPercent(topVehicle.risk_percent) : "N/A",
      meta: "Most urgent vehicle in queue",
    },
    {
      label: "Live fleet",
      value: `${fleet.length}`,
      meta: "Vehicles actively monitored",
    },
    {
      label: "Average risk",
      value: formatPercent(liveRiskAvg * 100, 1),
      meta: "Current fleet-wide failure probability",
    },
  ];

  return (
    <div className="app-shell">
      <div className="backdrop backdrop-a" />
      <div className="backdrop backdrop-b" />

      <header className="topbar">
        <div>
          <span className="eyebrow">EV Predictive Maintenance</span>
          <div className="brand-row">
            <div className="brand-mark">EV</div>
            <div>
              <h1>Fleet Pulse Control Room</h1>
              <p>{activeTabData?.kicker}</p>
            </div>
          </div>
        </div>

        <div className="status-cluster">
          <div className="status-pill">
            <span className="status-dot" />
            Auto-refresh every 5s
          </div>
          <div className="status-pill strong">{formatPercent(health)} fleet health</div>
        </div>
      </header>

      <div className="hero-grid">
        <section className="hero-panel">
          <div className="hero-copy">
            <span className="eyebrow">Live command overview</span>
            <h2>Distinct view, same EV theme, sharper hierarchy.</h2>
            <p>
              Monitor failure probability, component health, maintenance cost, and
              action priorities from one responsive mission-style dashboard.
            </p>
          </div>

          <div className="hero-metrics">
            <div className="hero-ring">
              <div className="hero-ring-inner">
                <span>Failure risk</span>
                <strong>{formatPercent(failureRisk, 1)}</strong>
              </div>
            </div>

            <div className="hero-summary">
              <div>
                <span className="metric-label">Remaining useful life</span>
                <strong>{analysis.predicted_rul_hours}h</strong>
              </div>
              <div>
                <span className="metric-label">Estimated range</span>
                <strong>{analysis.range_prediction} km</strong>
              </div>
              <div>
                <span className="metric-label">Charging guidance</span>
                <strong>{analysis.charging_advice}</strong>
              </div>
            </div>
          </div>
        </section>

        <aside className="signal-panel">
          {signalCards.map((card) => (
            <div key={card.label} className="signal-card">
              <span>{card.label}</span>
              <strong>{card.value}</strong>
              <p>{card.meta}</p>
            </div>
          ))}
        </aside>
      </div>

      <nav className="tabbar" aria-label="Dashboard sections">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? "tab active" : "tab"}
            onClick={() => setActiveTab(tab.id)}
          >
            <span>{tab.label}</span>
            <small>{tab.kicker}</small>
          </button>
        ))}
      </nav>

      {error ? <div className="status-banner error">{error}</div> : null}

      {activeTab === "dashboard" && (
        <main className="content-grid">
          <section className="feature-card spotlight-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Fleet overview</span>
                <h3>Risk roster</h3>
              </div>
              <p>Live status with clear risk segmentation for every monitored EV.</p>
            </div>

            <div className="vehicle-board">
              {fleet.map((vehicle, index) => (
                <article
                  key={`${vehicle.id}-${index}`}
                  className={`vehicle-tile ${vehicle.risk.toLowerCase()}`}
                >
                  <div className="vehicle-tile-top">
                    <span className="vehicle-id">Vehicle {vehicle.id}</span>
                    <span className={`risk-tag ${vehicle.risk.toLowerCase()}`}>
                      {vehicle.risk}
                    </span>
                  </div>
                  <strong>{formatPercent(vehicle.probability * 100, 1)}</strong>
                  <p>Failure probability</p>
                </article>
              ))}
            </div>
          </section>

          <section className="feature-card compact-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Priority vehicle</span>
                <h3>Immediate attention</h3>
              </div>
            </div>

            <div className="attention-stack">
              <div className="attention-value">
                {topVehicle ? formatPercent(topVehicle.risk_percent) : "N/A"}
              </div>
              <p>Highest observed risk in the current scan.</p>
              <div className="mini-bar">
                <div
                  className="mini-bar-fill danger"
                  style={{ width: `${topVehicle?.risk_percent || 0}%` }}
                />
              </div>
            </div>
          </section>

          <section className="feature-card compact-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Operational score</span>
                <h3>Fleet resilience</h3>
              </div>
            </div>

            <div className="attention-stack">
              <div className="attention-value">{formatPercent(health)}</div>
              <p>Healthy fleet score based on accumulated vehicle risk.</p>
              <div className="mini-bar">
                <div className="mini-bar-fill" style={{ width: `${health}%` }} />
              </div>
            </div>
          </section>
        </main>
      )}

      {activeTab === "analytics" && (
        <main className="analytics-grid">
          <section className="feature-card chart-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Prediction flow</span>
                <h3>Live failure trend</h3>
              </div>
              <p>Snapshot of current fleet failure probability.</p>
            </div>

            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={fleet}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(151, 169, 255, 0.15)" />
                <XAxis dataKey="id" stroke="#9fb0ff" />
                <YAxis stroke="#9fb0ff" />
                <Tooltip
                  contentStyle={{
                    background: "#0f1631",
                    border: "1px solid rgba(79, 207, 255, 0.35)",
                    borderRadius: "14px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="probability"
                  stroke="#49e6ff"
                  strokeWidth={3}
                  dot={{ r: 4, fill: "#ff4d8d" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </section>

          <section className="feature-card chart-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Explainability</span>
                <h3>SHAP feature impact</h3>
              </div>
              <p>Signals with the largest contribution to model output.</p>
            </div>

            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={shapData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(151, 169, 255, 0.15)" />
                <XAxis
                  dataKey="name"
                  stroke="#9fb0ff"
                  angle={-25}
                  textAnchor="end"
                  height={80}
                />
                <YAxis stroke="#9fb0ff" />
                <Tooltip
                  contentStyle={{
                    background: "#0f1631",
                    border: "1px solid rgba(79, 207, 255, 0.35)",
                    borderRadius: "14px",
                  }}
                />
                <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="url(#impactGradient)" />
                <defs>
                  <linearGradient id="impactGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#49e6ff" />
                    <stop offset="100%" stopColor="#ff4d8d" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </section>

          <section className="feature-card timeline-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Recorded history</span>
                <h3>Recent vehicle log</h3>
              </div>
              <p>Last captured probability updates from persisted history.</p>
            </div>

            <div className="timeline-list">
              {historyTimeline.length ? (
                historyTimeline.map((item) => (
                  <div key={item.name} className="timeline-item">
                    <span>{item.name}</span>
                    <strong>{formatPercent(item.probability, 1)}</strong>
                  </div>
                ))
              ) : (
                <p className="empty-copy">No recorded history available yet.</p>
              )}
            </div>
          </section>
        </main>
      )}

      {activeTab === "vehicle" && (
        <main className="content-grid">
          <section className="feature-card spotlight-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Vehicle diagnostics</span>
                <h3>Core performance indicators</h3>
              </div>
              <p>Detailed health, range, and predicted maintenance timing.</p>
            </div>

            <div className="metric-grid">
              <article className="metric-tile">
                <span>Failure risk</span>
                <strong>{formatPercent(failureRisk, 2)}</strong>
                <p>Predicted probability of failure.</p>
              </article>
              <article className="metric-tile">
                <span>RUL</span>
                <strong>{analysis.predicted_rul_hours}h</strong>
                <p>Estimated hours until maintenance window.</p>
              </article>
              <article className="metric-tile">
                <span>Range</span>
                <strong>{analysis.range_prediction} km</strong>
                <p>Projected distance remaining.</p>
              </article>
              <article className="metric-tile">
                <span>Health score</span>
                <strong>{formatPercent(analysis.vehicle_health?.overall_health)}</strong>
                <p>Composite system condition score.</p>
              </article>
            </div>
          </section>

          <section className="feature-card half-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Component health</span>
                <h3>Subsystem readiness</h3>
              </div>
            </div>

            <div className="component-stack">
              {[
                ["Battery", analysis.vehicle_health?.battery_health],
                ["Motor", analysis.vehicle_health?.motor_health],
                ["Brake", analysis.vehicle_health?.brake_health],
              ].map(([label, value]) => (
                <div key={label} className="component-row">
                  <div className="component-copy">
                    <span>{label}</span>
                    <strong>{formatPercent(value)}</strong>
                  </div>
                  <div className="component-track">
                    <div className="component-progress" style={{ width: `${value || 0}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="feature-card half-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Alerts</span>
                <h3>Active warnings</h3>
              </div>
              <p>Fast signal checks for anomalies that need operator attention.</p>
            </div>

            <div className="alert-panel">
              <div className="alert-panel-header">
                <div>
                  <span className="alert-panel-label">Diagnostic status</span>
                  <strong>
                    {analysis.alerts?.length
                      ? `${analysis.alerts.length} active alert${
                          analysis.alerts.length > 1 ? "s" : ""
                        }`
                      : "System stable"}
                  </strong>
                </div>
                <span
                  className={
                    analysis.alerts?.length ? "alert-state alert" : "alert-state clear"
                  }
                >
                  {analysis.alerts?.length ? "Attention needed" : "No alert"}
                </span>
              </div>

              <div className="alert-stack">
              {analysis.alerts?.length ? (
                analysis.alerts.map((alert, index) => (
                  <div key={`${alert}-${index}`} className="alert-row">
                    <span className="alert-bullet" />
                    <div className="alert-copy">
                      <strong>Alert {String(index + 1).padStart(2, "0")}</strong>
                      <p>{alert}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="alert-row ok">
                  <span className="alert-bullet ok" />
                  <div className="alert-copy">
                    <strong>Nominal state</strong>
                    <p>No active alerts for this vehicle snapshot.</p>
                  </div>
                </div>
              )}
              </div>
            </div>
          </section>
        </main>
      )}

      {activeTab === "maintenance" && (
        <main className="content-grid">
          <section className="feature-card spotlight-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Maintenance strategy</span>
                <h3>Cost and intervention planning</h3>
              </div>
              <p>Compare cost impact and prioritize the next service action.</p>
            </div>

            <div className="cost-panels">
              <article className="cost-tile">
                <span>Act now</span>
                <strong>{formatCurrency(analysis.maintenance_cost?.cost_now)}</strong>
                <p>Recommended immediate intervention cost.</p>
              </article>
              <article className="cost-tile warning">
                <span>Delay action</span>
                <strong>{formatCurrency(analysis.maintenance_cost?.cost_delayed)}</strong>
                <p>Escalated cost if the issue is postponed.</p>
              </article>
            </div>
          </section>

          <section className="feature-card spotlight-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Recommendations</span>
                <h3>Suggested next steps</h3>
              </div>
            </div>

            <div className="recommendation-list">
              {analysis.recommendations?.map((recommendation, index) => (
                <div key={`${recommendation}-${index}`} className="recommendation-row">
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <p>{recommendation}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="feature-card compact-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Charging</span>
                <h3>Battery guidance</h3>
              </div>
            </div>
            <p className="highlight-copy">{analysis.charging_advice}</p>
          </section>

          <section className="feature-card compact-card">
            <div className="section-heading">
              <div>
                <span className="eyebrow">Risk by component</span>
                <h3>Subsystem priority</h3>
              </div>
            </div>

            <div className="risk-list">
              {Object.entries(analysis.component_risk || {}).map(([component, risk]) => (
                <div key={component} className="risk-row">
                  <span>{component}</span>
                  <strong className={risk.toLowerCase()}>{risk}</strong>
                </div>
              ))}
            </div>
          </section>
        </main>
      )}
    </div>
  );
}

export default App;
