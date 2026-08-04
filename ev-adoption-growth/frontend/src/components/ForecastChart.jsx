import React from 'react';
import { Line } from 'react-chartjs-2';

const ForecastChart = ({ data }) => {
  if (!data) return <div className="loader"></div>;

  const chartData = {
    labels: data.years,
    datasets: [{
      label: 'EV Adoption Forecast',
      data: data.predictions,
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.1)',
      borderWidth: 3,
      tension: 0.4,
      fill: true,
      pointRadius: 4,
      pointHoverRadius: 6
    }]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: true, position: 'top' },
      tooltip: {
        callbacks: {
          label: (context) => `${context.parsed.y.toLocaleString()} EVs`
        }
      }
    },
    scales: {
      y: {
        ticks: {
          callback: (value) => value.toLocaleString()
        }
      }
    }
  };

  return (
    <section className="card chart-card">
      <h2 className="card-title">📈 EV Adoption Growth Forecast (2015-2035)</h2>
      <Line data={chartData} options={options} />
    </section>
  );
};

export default ForecastChart;
