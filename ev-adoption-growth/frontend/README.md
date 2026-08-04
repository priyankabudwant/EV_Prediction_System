# React Frontend - Component Structure

## 📁 Project Structure

```
frontend/src/
├── components/
│   ├── Header.jsx              # Dashboard header
│   ├── PredictionCard.jsx      # Future prediction form
│   ├── Top5GrowthCard.jsx      # Top 5 growing categories
│   ├── CO2ReductionCard.jsx    # CO2 reduction impact
│   ├── ComparisonChart.jsx     # 2W vs 4W line chart
│   ├── TrendChart.jsx          # Overall trend bar chart
│   ├── Footer.jsx              # Footer component
│   └── Loader.jsx              # Loading spinner
├── services/
│   └── api.js                  # API service layer
├── App.js                      # Main app component
├── App.css                     # Styles
└── index.js                    # Entry point
```

## 🚀 Setup & Run

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm start
```

### 3. Build for Production
```bash
npm run build
```

## 🔧 Backend Required

Make sure Flask backend is running on port 5000:
```bash
python app.py
```

## 📦 Components Overview

- **Header**: Title and subtitle
- **PredictionCard**: Category/year selection with prediction
- **Top5GrowthCard**: Displays top 5 growing categories
- **CO2ReductionCard**: Shows CO2 reduction data
- **ComparisonChart**: Line chart for 2W vs 4W
- **TrendChart**: Bar chart for overall trend
- **Footer**: Copyright info
- **Loader**: Loading state

## 🎨 Features

✅ Modular component architecture
✅ Separate API service layer
✅ Responsive design
✅ Animated transitions
✅ Chart.js integration
✅ Error handling
