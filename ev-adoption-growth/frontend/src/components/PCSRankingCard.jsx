import React from 'react';
import { Bar } from 'react-chartjs-2';

const PCSRankingCard = ({ data }) => {
  if (!data || data.length === 0) return <div className="loader"></div>;

  const chartData = {
    labels: data.map(item => item.State),
    datasets: [{
      label: 'Operational PCS',
      data: data.map(item => item['No. of Operational PCS']),
      backgroundColor: 'rgba(255, 159, 64, 0.8)',
      borderColor: 'rgb(255, 159, 64)',
      borderWidth: 2,
      borderRadius: 8
    }]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    indexAxis: 'y',
    plugins: {
      legend: { display: false }
    },
    scales: {
      x: {
        ticks: {
          callback: (value) => value.toLocaleString()
        }
      }
    }
  };

  return (
    <section className="card chart-card">
      <h2 className="card-title">🏆 State-wise Charging Infrastructure Ranking</h2>
      <Bar data={chartData} options={options} />
    </section>
  );
};

export default PCSRankingCard;
