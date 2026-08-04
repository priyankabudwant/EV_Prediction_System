import React from 'react';
import { Bar } from 'react-chartjs-2';

const TrendChart = ({ data }) => {
  if (!data) return <div className="loader"></div>;

  const chartData = {
    labels: data.years,
    datasets: [{
      label: 'Total EV Registrations',
      data: data.total,
      backgroundColor: 'rgba(102, 126, 234, 0.8)',
      borderColor: 'rgb(102, 126, 234)',
      borderWidth: 2,
      borderRadius: 8
    }]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { display: true, position: 'top' }
    }
  };

  return (
    <section className="card chart-card">
      <h2 className="card-title">📈 Overall EV Adoption Trend</h2>
      <Bar data={chartData} options={options} />
    </section>
  );
};

export default TrendChart;
