import React from "react";
import { Bar } from "react-chartjs-2";

const CAGRChart = ({ cagrData }) => {
  if (!cagrData) return null;

  const data = {
    labels: cagrData.map(item => item.category),
    datasets: [
      {
        label: "CAGR %",
        data: cagrData.map(item => item.cagr),
        backgroundColor: "#00c9ff"
      }
    ]
  };

  return (
    <div className="card">
      <h2>📊 Category CAGR Ranking</h2>
      <Bar data={data} options={chartOptions} />
    </div>
  );
};

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { labels: { color: "white" } }
  },
  scales: {
    x: { ticks: { color: "white" } },
    y: { ticks: { color: "white" } }
  }
};

export default CAGRChart;
