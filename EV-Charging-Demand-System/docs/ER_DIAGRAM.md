# EV Charging Demand System ER Diagram

This project currently uses CSV files and API data models rather than a relational database. The diagram below represents the entities implied by the datasets and prediction workflow, and can be used as a reference if the project is later moved to a database.

```mermaid
erDiagram
    STATE ||--o{ CITY : contains
    CITY ||--o{ CHARGING_STATION : has
    CITY ||--o{ CITY_DEMAND_METRIC : measures
    CITY ||--o{ DEMAND_PREDICTION : receives
    PREDICTION_SCENARIO ||--o{ DEMAND_PREDICTION : generates

    STATE {
        int state_id PK
        string name
    }

    CITY {
        int city_id PK
        int state_id FK
        string name
        decimal latitude
        decimal longitude
        int population_density
    }

    CHARGING_STATION {
        int station_id PK
        int city_id FK
        string name
        string address
        string operator
        string usage_type
        string connector_type
        decimal power_kw
        decimal latitude
        decimal longitude
        int charger_count
        int fast_charger_count
        decimal renewable_energy_share
        string predicted_peak_hour
        string maintenance_risk
    }

    CITY_DEMAND_METRIC {
        int metric_id PK
        int city_id FK
        int charger_count
        decimal fast_ratio
        int avg_sessions
        decimal occupancy
        decimal ev_growth
        decimal demand_index
        string demand_level
    }

    PREDICTION_SCENARIO {
        int scenario_id PK
        int charger_count
        decimal fast_ratio
        int avg_sessions
        decimal occupancy
        decimal ev_growth
        int population_density
        datetime created_at
    }

    DEMAND_PREDICTION {
        int prediction_id PK
        int scenario_id FK
        int city_id FK
        decimal score
        decimal normalized_score
        string demand_level
        datetime predicted_at
    }
```

## Source Mapping

- `STATE`, `CITY`, and `CITY_DEMAND_METRIC` come from `backend/city_demand_index.csv`.
- `CHARGING_STATION` comes from `backend/data/Indian_EV_Stations_Simplified.csv` and `backend/data/Indian_EV_Stations_Simplified1.csv`.
- `PREDICTION_SCENARIO` maps to the FastAPI `InputData` request model in `backend/main.py`.
- `DEMAND_PREDICTION` maps to the `/predict` response generated in `backend/main.py`.

