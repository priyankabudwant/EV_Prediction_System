import React, { useEffect, useMemo, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./Dashboard.css";

const initialChartData = [
  { time: "08:00", demand: 90 },
  { time: "09:00", demand: 120 },
  { time: "10:00", demand: 105 },
  { time: "11:00", demand: 140 },
  { time: "12:00", demand: 160 },
  { time: "13:00", demand: 130 },
  { time: "14:00", demand: 175 },
  { time: "15:00", demand: 150 },
];

const navigationCards = [
  {
    label: "Open Failure Dashboard",
    eyebrow: "Reliability",
    description: "Inspect faults, anomaly traces, and station failure signals.",
    accent: "rose",
    url: "http://localhost:3001",
  },
  {
    label: "EV Demand",
    eyebrow: "Forecasting",
    description: "Explore charging demand pressure and utilization movement.",
    accent: "amber",
    url: "http://localhost:3003",
  },
  {
    label: "EV Adoption",
    eyebrow: "Market Shift",
    description: "Track adoption growth, conversion momentum, and expansion pace.",
    accent: "mint",
    url: "http://localhost:3002",
  },
  {
    label: "EV Cost-Carbon",
    eyebrow: "Sustainability",
    description: "Compare operating cost and carbon impact across charging scenarios.",
    accent: "sky",
    url: "http://localhost:3004",
  },
];

function Dashboard() {
  const [batteryHealth, setBatteryHealth] = useState(85);
  const [demand] = useState(120);
  const [carbonSaved] = useState(45);
  const [chartData] = useState(initialChartData);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/fleet")
      .then((res) => res.json())
      .then((data) => {
        if (typeof data?.battery_health === "number") {
          setBatteryHealth(data.battery_health);
        }
      })
      .catch(() => {
        // Keep local fallback values when the API is unavailable.
      });
  }, []);

  const avgDemand = useMemo(() => {
    const total = chartData.reduce((sum, item) => sum + item.demand, 0);
    return Math.round(total / chartData.length);
  }, [chartData]);

  const peakDemand = useMemo(
    () => Math.max(...chartData.map((item) => item.demand)),
    [chartData]
  );

  const systemStatus = batteryHealth >= 80 ? "Stable" : "Monitor";
  const batteryArcStyle = { "--battery-fill": `${Math.max(0, Math.min(100, batteryHealth))}%` };
  const demandArcStyle = { "--demand-fill": `${Math.min(100, Math.round((demand / 200) * 100))}%` };

  return (
    <main className="dashboard-shell">
      <div className="dashboard-noise" />
      <div className="dashboard-frame">
        <section className="dashboard-hero">
          <div className="hero-copy">
            <p className="eyebrow">Green mobility command center</p>
            <h1>
              <span className="hero-brand">GREEN VOLT AI</span>
              <span className="hero-title-subtitle">EV intelligence dashboard</span>
            </h1>
            <p className="hero-text">
              Operations, forecasting, sustainability, and system health are now
              organized into a clearer front page so the dashboard feels structured,
              readable, and presentation-ready across desktop, tablet, and mobile.
            </p>

            <div className="hero-kpis">
              <article className="hero-kpi-card">
                <span>Battery health</span>
                <strong>{batteryHealth}%</strong>
              </article>
              <article className="hero-kpi-card">
                <span>Average demand</span>
                <strong>{avgDemand} kWh</strong>
              </article>
              <article className="hero-kpi-card">
                <span>Carbon saved</span>
                <strong>{carbonSaved} kg</strong>
              </article>
            </div>

            <div className="hero-meta">
              <div className="live-badge">
                <span className="live-dot" />
                Live telemetry
              </div>
              <p className="meta-note">
                Navigation actions remain mapped to the same module destinations.
              </p>
            </div>
          </div>

          <div className="hero-orbit">
            <div className="hero-orbit-top">
              <div className="status-panel">
                <div className="status-panel-top">
                  <p className="status-label">Fleet pulse</p>
                  <span className={`status-chip status-chip-${systemStatus.toLowerCase()}`}>
                    {systemStatus}
                  </span>
                </div>
                <div className="status-panel-body">
                  <strong>{batteryHealth}%</strong>
                  <span>Battery confidence holding inside the healthy operating band.</span>
                </div>
              </div>
            </div>

            <div className="hero-orbit-center">
              <div className="orbit-ring orbit-ring-one" />
              <div className="orbit-ring orbit-ring-two" />
              <div className="orbit-core" />
            </div>

            <div className="hero-orbit-bottom">
              <div className="orbit-panel orbit-panel-bottom">
                <p>Module count</p>
                <strong>{navigationCards.length}</strong>
                <span>Linked dashboards ready to open</span>
              </div>
              <div className="orbit-panel orbit-panel-side">
                <p>Peak load</p>
                <strong>{peakDemand} kWh</strong>
                <span>Today&apos;s highest charging window</span>
              </div>
            </div>
          </div>
        </section>

        <section className="dashboard-grid">
          <article className="panel panel-feature">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Energy posture</p>
                <h2>System overview</h2>
              </div>
              <span className="panel-tag">AI monitored</span>
            </div>

            <div className="radial-metrics">
              <div className="radial-card">
                <div className="radial-gauge battery-gauge" style={batteryArcStyle}>
                  <div className="radial-center">
                    <strong>{batteryHealth}%</strong>
                    <span>Battery</span>
                  </div>
                </div>
                <p>Battery health is tracking inside the healthy band.</p>
              </div>

              <div className="radial-card">
                <div className="radial-gauge demand-gauge" style={demandArcStyle}>
                  <div className="radial-center">
                    <strong>{demand} kWh</strong>
                    <span>Demand</span>
                  </div>
                </div>
                <p>Demand load remains aligned with the current schedule envelope.</p>
              </div>
            </div>

            <div className="signal-list">
              <div className="signal-item">
                <span>Carbon saved</span>
                <strong>{carbonSaved} kg CO2</strong>
              </div>
              <div className="signal-item">
                <span>Average demand</span>
                <strong>{avgDemand} kWh</strong>
              </div>
              <div className="signal-item">
                <span>Automation status</span>
                <strong>{systemStatus}</strong>
              </div>
            </div>

            <div className="feature-note">
              <span className="feature-line" />
              <p>
                The left column now stays compact and readable while the chart and
                module launcher get the width they need.
              </p>
            </div>
          </article>

          <article className="panel panel-map">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Load terrain</p>
                <h2>Demand storyline</h2>
              </div>
              <span className="panel-tag">8 checkpoints</span>
            </div>

            <div className="terrain-summary">
              <div>
                <span className="summary-label">Load crest</span>
                <strong>{peakDemand} kWh</strong>
              </div>
              <div>
                <span className="summary-label">Mean flow</span>
                <strong>{avgDemand} kWh</strong>
              </div>
            </div>

            <div className="chart-frame">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <defs>
                    <linearGradient id="dashboardLine" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stopColor="#ff7a18" />
                      <stop offset="50%" stopColor="#ffd166" />
                      <stop offset="100%" stopColor="#24c6a8" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(255,255,255,0.08)" strokeDasharray="4 4" />
                  <XAxis
                    dataKey="time"
                    stroke="rgba(255,255,255,0.45)"
                    tickLine={false}
                    axisLine={false}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis
                    stroke="rgba(255,255,255,0.45)"
                    tickLine={false}
                    axisLine={false}
                    tick={{ fontSize: 12 }}
                  />
                  <Tooltip
                    cursor={{ stroke: "rgba(255,255,255,0.12)" }}
                    contentStyle={{
                      background: "#102235",
                      border: "1px solid rgba(255,255,255,0.12)",
                      borderRadius: "16px",
                      color: "#f8fafc",
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="demand"
                    stroke="url(#dashboardLine)"
                    strokeWidth={4}
                    dot={{ fill: "#fff4d6", stroke: "#ff9f45", strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6, fill: "#24c6a8" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </article>

          <article className="panel panel-nav">
            <div className="panel-header panel-header-stack">
              <div>
                <p className="eyebrow">Prediction modules</p>
                <h2>Quick launch deck</h2>
              </div>
              <p className="panel-caption">
                Four modules are arranged in an even launcher grid so the section no
                longer feels broken when cards wrap.
              </p>
            </div>

            <div className="nav-card-grid">
              {navigationCards.map((card) => (
                <button
                  key={card.label}
                  type="button"
                  className={`nav-launch nav-launch-${card.accent}`}
                  onClick={() => {
                    window.location.href = card.url;
                  }}
                >
                  <span className="nav-launch-top">{card.eyebrow}</span>
                  <strong>{card.label}</strong>
                  <p>{card.description}</p>
                  <span className="nav-launch-cta">Open module</span>
                </button>
              ))}
            </div>
          </article>
        </section>
      </div>
    </main>
  );
}

export default Dashboard;
