import React from "react";
import { Bar } from "react-chartjs-2";

const Top5Chart = ({ top5Growth }) => {
  if (!top5Growth) return null;

  const data = {
    labels: top5Growth.map(item => item.category),
    datasets: [
      {
        label: "Growth by 2035",
        data: top5Growth.map(item => item.growth),
        backgroundColor: [
          "#667eea",
          "#764ba2",
          "#00f2fe",
          "#f5576c",
          "#4facfe"
        ]
      }
    ]
  };

  return (
    <div className="card" id="top5">
      <h2>🚀 Top 5 Growing Categories</h2>
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

export default Top5Chart;
