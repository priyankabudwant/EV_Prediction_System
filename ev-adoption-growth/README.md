# EV Adoption Growth Dashboard

A modern, responsive web application for analyzing and predicting Electric Vehicle adoption trends.

## Features

- 🔮 **Future Prediction**: Predict EV registrations for any category and year
- 🚀 **Top 5 Growth Analysis**: View the fastest-growing EV categories by 2035
- 🌱 **CO2 Reduction Impact**: Calculate environmental impact of EV adoption
- 📊 **2W vs 4W Comparison**: Compare two-wheeler and four-wheeler trends
- 📈 **Overall Trend Analysis**: Visualize total EV adoption over time

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your data files are in the `data/` directory:
   - ev_cat_01-24.csv
   - EV Maker by Place.csv
   - ev_sales_by_makers_and_cat_15-24.csv
   - OperationalPC.csv
   - Vehicle Class - All.csv

3. Ensure trained models are in the `models/` directory:
   - category_future_model1.pkl

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
ev-adoption-growth/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Responsive CSS with animations
│   └── script.js         # JavaScript for API calls and charts
├── data/                 # CSV data files
├── models/               # Trained ML models
├── src/                  # Analysis scripts
└── requirements.txt      # Python dependencies
```

## API Endpoints

- `GET /` - Main dashboard
- `POST /api/predict` - Predict future values
- `GET /api/top5-growth` - Get top 5 growing categories
- `GET /api/co2-reduction` - Get CO2 reduction estimates
- `GET /api/2w-vs-4w` - Get 2W vs 4W comparison data
- `GET /api/categories` - Get available categories
- `GET /api/yearly-trend` - Get overall yearly trend

## Technologies Used

- **Backend**: Flask, Pandas, NumPy, Scikit-learn, Joblib
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Design**: Gradient backgrounds, animations, responsive layout

## Features Highlights

- ✨ Modern gradient design with smooth animations
- 📱 Fully responsive for mobile, tablet, and desktop
- 🎨 Colorful and attractive UI with hover effects
- ⚡ Fast API responses with efficient data processing
- 📊 Interactive charts with Chart.js

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

MIT License
