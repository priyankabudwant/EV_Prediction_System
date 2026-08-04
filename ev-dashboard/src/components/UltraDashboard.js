import React, { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

function AdvancedDashboard() {

  const [battery, setBattery] = useState(82);
  const [demand, setDemand] = useState(120);
  const [carbon, setCarbon] = useState(56);
  const [risk, setRisk] = useState("Low");

  const [data, setData] = useState([]);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {

      setBattery(prev => Math.max(50, prev + (Math.random()*4 - 2)));
      setDemand(prev => prev + Math.floor(Math.random()*10));
      setCarbon(prev => prev + Math.floor(Math.random()*5));

      setData(prev => [
        ...prev.slice(-6),
        { time: new Date().toLocaleTimeString(), demand: demand }
      ]);

    }, 3000);

    return () => clearInterval(interval);
  }, [demand]);

  return (
    <div style={container}>

      <h1 style={{color:"#00e6e6"}}>⚡ EV AI Intelligence Dashboard</h1>

      {/* KPI GRID */}
      <div style={grid}>

        {/* Battery Gauge */}
        <div style={card}>
          <h3>🔋 Battery Health</h3>
          <div style={{width:120, margin:"auto"}}>
            <CircularProgressbar
              value={battery}
              text={`${battery.toFixed(0)}%`}
              styles={buildStyles({
                pathColor: "#00ffcc",
                textColor: "#fff",
                trailColor: "#333"
              })}
            />
          </div>
        </div>

        {/* Demand */}
        <div style={card}>
          <h3>⚡ Charging Demand</h3>
          <h2>{demand} kWh</h2>
        </div>

        {/* Carbon */}
        <div style={card}>
          <h3>🌍 Carbon Saved</h3>
          <h2>{carbon} kg</h2>
        </div>

        {/* AI Prediction */}
        <div style={card}>
          <h3>🤖 AI Risk Status</h3>
          <h2 style={{color: risk === "High" ? "red" : "#00ffcc"}}>
            {risk}
          </h2>
          <p>Battery stable. No immediate failure predicted.</p>
        </div>

      </div>

      {/* CHART */}
      <div style={chartCard}>

        <h3>📊 Real-Time Demand Trend</h3>

        <LineChart width={800} height={300} data={data}>
          <CartesianGrid stroke="#444" />
          <XAxis dataKey="time" stroke="#ccc" />
          <YAxis stroke="#ccc" />
          <Tooltip />
          <Line type="monotone" dataKey="demand" stroke="#00e6e6" />
        </LineChart>

      </div>

    </div>
  );
}

/* 🎨 STYLES */

const container = {
  background: "#0d1117",
  minHeight: "100vh",
  padding: "20px",
  color: "white",
  fontFamily: "Arial"
};

const grid = {
  display: "grid",
  gridTemplateColumns: "repeat(4, 1fr)",
  gap: "20px",
  marginBottom: "30px"
};

const card = {
  background: "#161b22",
  padding: "20px",
  borderRadius: "15px",
  textAlign: "center",
  boxShadow: "0 0 15px rgba(0,255,200,0.2)"
};

const chartCard = {
  background: "#161b22",
  padding: "20px",
  borderRadius: "15px",
  boxShadow: "0 0 15px rgba(0,255,200,0.2)"
};

export default AdvancedDashboard;