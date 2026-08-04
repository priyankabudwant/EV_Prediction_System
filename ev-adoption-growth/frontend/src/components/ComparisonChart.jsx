import React from 'react';
import { Line } from 'react-chartjs-2';

const ComparisonChart = ({ data }) => {
  if (!data) return <div className="loader"></div>;

  const chartData = {
    labels: data.years,
    datasets: [
      {
        label: 'Two Wheeler',
        data: data.two_wheeler,
        borderColor: 'rgb(102, 126, 234)',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        borderWidth: 3,
        tension: 0.4,
        fill: true
      },
      {
        label: 'Four Wheeler',
        data: data.four_wheeler,
        borderColor: 'rgb(245, 87, 108)',
        backgroundColor: 'rgba(245, 87, 108, 0.1)',
        borderWidth: 3,
        tension: 0.4,
        fill: true
      }
    ]
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
      <h2 className="card-title">📊 Two Wheeler vs Four Wheeler Comparison</h2>
      <Line data={chartData} options={options} />
    </section>
  );
};

export default ComparisonChart;
