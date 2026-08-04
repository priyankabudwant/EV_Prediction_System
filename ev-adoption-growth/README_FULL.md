# EV Adoption Growth Dashboard

A modern, responsive web application for analyzing and predicting Electric Vehicle adoption trends.

## 🎨 Two Frontend Options

### Option 1: Vanilla JavaScript (Simple Setup)
Located in `templates/` and `static/`

### Option 2: React (Modern Framework) ⭐ Recommended
Located in `frontend/`

---

## 🚀 Quick Start

### Backend Setup (Required for Both)

1. **Install Python dependencies:**
```bash
pip install flask flask-cors pandas numpy scikit-learn joblib
```

2. **Ensure data files are in `data/` directory:**
   - ev_cat_01-24.csv
   - EV Maker by Place.csv
   - ev_sales_by_makers_and_cat_15-24.csv
   - OperationalPC.csv
   - Vehicle Class - All.csv

3. **Ensure trained model is in `models/` directory:**
   - category_future_model1.pkl

4. **Start Flask backend:**
```bash
python app.py
```
Backend runs on: `http://localhost:5000`

---

## Option 1: Vanilla JavaScript Frontend

**Already set up!** Just open browser to:
```
http://localhost:5000
```

---

## Option 2: React Frontend (Recommended)

### Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start React development server:**
```bash
npm start
```

React app runs on: `http://localhost:3000`

### Build for Production
```bash
npm run build
```

---

## ✨ Features

- 🔮 **Future Prediction**: Predict EV registrations for any category and year
- 🚀 **Top 5 Growth Analysis**: View the fastest-growing EV categories by 2035
- 🌱 **CO2 Reduction Impact**: Calculate environmental impact of EV adoption
- 📊 **2W vs 4W Comparison**: Compare two-wheeler and four-wheeler trends
- 📈 **Overall Trend Analysis**: Visualize total EV adoption over time

## 🛠️ Technologies

### Backend
- Flask
- Pandas, NumPy
- Scikit-learn, Joblib
- Flask-CORS

### Frontend (React)
- React 18
- Chart.js & react-chartjs-2
- Axios
- Modern CSS with animations

### Frontend (Vanilla)
- HTML5, CSS3, JavaScript
- Chart.js

## 📊 API Endpoints

- `GET /` - Main dashboard (Vanilla JS)
- `POST /api/predict` - Predict future values
- `GET /api/top5-growth` - Get top 5 growing categories
- `GET /api/co2-reduction` - Get CO2 reduction estimates
- `GET /api/2w-vs-4w` - Get 2W vs 4W comparison data
- `GET /api/categories` - Get available categories
- `GET /api/yearly-trend` - Get overall yearly trend

## 🎨 Design Features

- ✨ Modern gradient design with smooth animations
- 📱 Fully responsive for mobile, tablet, and desktop
- 🎨 Colorful and attractive UI with hover effects
- ⚡ Fast API responses with efficient data processing
- 📊 Interactive charts

## 🌐 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 📝 License

MIT License
