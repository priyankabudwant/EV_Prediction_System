import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function DemandChart({ predictions }) {
  const counts = { Low: 0, Medium: 0, High: 0 };

  Object.values(predictions).forEach((prediction) => {
    const level = prediction.demand_level || prediction.level;
    if (counts[level] !== undefined) {
      counts[level] += 1;
    }
  });

  return (
    <section className="panel-surface chart-panel">
      <div className="panel-heading">
        <p className="eyebrow">Demand Overview</p>
        <h2>Distribution Snapshot</h2>
      </div>

      <div className="chart-wrap">
        <Bar
          data={{
            labels: ["Low", "Medium", "High"],
            datasets: [
              {
                label: "EV Charging Demand",
                data: [counts.Low, counts.Medium, counts.High],
                backgroundColor: ["#6ee7b7", "#fbbf24", "#f97316"],
                borderRadius: 10,
                borderSkipped: false,
              },
            ],
          }}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: "top",
                labels: {
                  color: "#d4e7e1",
                },
              },
              title: { display: false },
            },
            scales: {
              x: {
                ticks: { color: "#d4e7e1" },
                grid: { display: false },
              },
              y: {
                beginAtZero: true,
                ticks: {
                  color: "#d4e7e1",
                  precision: 0,
                },
                grid: {
                  color: "rgba(148, 163, 184, 0.15)",
                },
              },
            },
          }}
        />
      </div>
    </section>
  );
}
