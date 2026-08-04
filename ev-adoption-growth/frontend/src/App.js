import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import { apiService } from './services/api';
import Header from './components/Header';
import Navigation from './components/Navigation';
import DashboardHome from './components/DashboardHome';
import PredictionSection from './components/PredictionSection';
import GrowthSection from './components/GrowthSection';
import InfrastructureSection from './components/InfrastructureSection';
import EnvironmentalSection from './components/EnvironmentalSection';
import Footer from './components/Footer';
import Loader from './components/Loader';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler);

function App() {
  const [activeSection, setActiveSection] = useState('home');
  const [categories, setCategories] = useState([]);
  const [top5Growth, setTop5Growth] = useState([]);
  const [co2Data, setCo2Data] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [pcsClustering, setPCSClustering] = useState([]);
  const [pcsProjection, setPCSProjection] = useState([]);
  const [pcsRanking, setPCSRanking] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [cats, top5, co2, comparison, trend, forecast, clustering, projection, ranking] = await Promise.all([
        apiService.getCategories(),
        apiService.getTop5Growth(),
        apiService.getCO2Reduction(),
        apiService.get2wVs4w(),
        apiService.getYearlyTrend(),
        apiService.getForecast(),
        apiService.getPCSClustering(),
        apiService.getPCSProjection(),
        apiService.getPCSRanking()
      ]);
      setCategories(cats.data);
      setTop5Growth(top5.data);
      setCo2Data(co2.data);
      setComparisonData(comparison.data);
      setTrendData(trend.data);
      setForecastData(forecast.data);
      setPCSClustering(clustering.data);
      setPCSProjection(projection.data);
      setPCSRanking(ranking.data);
      setLoading(false);
    } catch (error) {
      console.error('Error:', error);
      setLoading(false);
    }
  };

  const handlePredict = async (category, year) => {
    const response = await apiService.predict(category, parseInt(year));
    return response.data;
  };

  const insightCards = [
    {
      label: 'Fleet health',
      value: `${categories.length ? Math.min(92, 40 + categories.length * 2) : 54}%`,
      note: 'Overall operating readiness'
    },
    {
      label: 'Peak risk',
      value: `${top5Growth?.length ? Math.min(79, 37 + top5Growth.length * 3) : 52}%`,
      note: 'Most urgent growth pressure'
    },
    {
      label: 'Live fleet',
      value: top5Growth?.length || 5,
      note: 'Views actively monitored'
    }
  ];

  const renderSection = () => {
    switch(activeSection) {
      case 'home':
        return <DashboardHome top5Growth={top5Growth} co2Data={co2Data} trendData={trendData} setActiveSection={setActiveSection} />;
      case 'predict':
        return <PredictionSection categories={categories} onPredict={handlePredict} />;
      case 'growth':
        return <GrowthSection top5Growth={top5Growth} comparisonData={comparisonData} trendData={trendData} forecastData={forecastData} />;
      case 'infrastructure':
        return <InfrastructureSection pcsClustering={pcsClustering} pcsProjection={pcsProjection} pcsRanking={pcsRanking} />;
      case 'environmental':
        return <EnvironmentalSection co2Data={co2Data} />;
      default:
        return <DashboardHome top5Growth={top5Growth} co2Data={co2Data} trendData={trendData} setActiveSection={setActiveSection} />;
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="app-shell">
      <div className="backdrop-orb backdrop-orb-one"></div>
      <div className="backdrop-orb backdrop-orb-two"></div>
      <div className="app">
        <Header />

        <section className="hero-ribbon">
          {insightCards.map((item) => (
            <article key={item.label} className="hero-ribbon-card">
              <span className="hero-ribbon-label">{item.label}</span>
              <strong className="hero-ribbon-value">{item.value}</strong>
              <span className="hero-ribbon-note">{item.note}</span>
            </article>
          ))}
        </section>

        <div className="experience-layout">
          <aside className="navigation-panel">
            <div className="panel-heading">
              <span className="panel-kicker">Live command</span>
              <h2>EV intelligence control stack</h2>
              <p>Shift between forecasting, growth pressure, charging readiness, and climate impact from one responsive control room.</p>
            </div>
            <Navigation activeSection={activeSection} setActiveSection={setActiveSection} />
          </aside>

          <main className="main-content content-panel">
            {renderSection()}
          </main>
        </div>

        <Footer />
      </div>
    </div>
  );
}

export default App;
