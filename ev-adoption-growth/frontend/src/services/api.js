import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const apiService = {
  getCategories: () => axios.get(`${API_BASE}/categories`),
  predict: (category, year) => axios.post(`${API_BASE}/predict`, { category, year }),
  getTop5Growth: () => axios.get(`${API_BASE}/top5-growth`),
  getCO2Reduction: () => axios.get(`${API_BASE}/co2-reduction`),
  get2wVs4w: () => axios.get(`${API_BASE}/2w-vs-4w`),
  getYearlyTrend: () => axios.get(`${API_BASE}/yearly-trend`),
  getForecast: () => axios.get(`${API_BASE}/forecast`),
  getPCSClustering: () => axios.get(`${API_BASE}/pcs-clustering`),
  getPCSProjection: () => axios.get(`${API_BASE}/pcs-projection`),
  getPCSRanking: () => axios.get(`${API_BASE}/pcs-ranking`)
};
