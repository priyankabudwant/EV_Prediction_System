import React, { useMemo, useState } from "react";
import axios from "axios";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import "./App.css";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8002";

const defaultFormData = {
  distance_km_per_day: 50,
  fuel_type: "petrol",
  vehicle_type: "4-wheeler",
  vehicle_age_years: 3,
  trip_days_per_year: 300,
  fuel_vehicle_mileage_kmpl: 15,
  fuel_price_per_liter: 105,
  ev_efficiency_kwh_per_km: 0.15,
  electricity_price_per_kwh: 8,
  grid_emission_factor: 0.82,
  fuel_emission_factor: 2.31,
  battery_health_percent: 92,
  home_charging_ratio: 0.8,
  public_charging_ratio: 0.2,
  fast_charging_ratio: 0.3,
  renewable_energy_usage_ratio: 0.2,
  annual_maintenance_cost_ev_rs: 5000,
  annual_maintenance_cost_fuel_rs: 12000,
  subsidy_amount_rs: 50000,
  road_tax_savings_rs: 10000,
  battery_capacity_kwh: 40,
  city_traffic_level: "medium",
  ac_usage_level: "4",
  charging_type: "fast-dominant",
  highway_ratio: 0.4,
  urban_ratio: 0.6,
  vehicle_purchase_cost_fuel_rs: 900000,
  vehicle_purchase_cost_ev_rs: 1400000,
};

const numberFields = new Set(
  Object.keys(defaultFormData).filter(
    (key) =>
      !["fuel_type", "vehicle_type", "city_traffic_level", "ac_usage_level", "charging_type"].includes(
        key
      )
  )
);

const steps = [
  {
    id: 0,
    title: "Choose prediction",
    caption: "Start by choosing the model and the kind of vehicle profile.",
  },
  {
    id: 1,
    title: "Travel profile",
    caption: "Only the day-to-day usage details that influence the prediction.",
  },
  {
    id: 2,
    title: "Charging and energy",
    caption: "Electricity, charging style, and battery condition.",
  },
  {
    id: 3,
    title: "Costs and ownership",
    caption: "Running cost and vehicle purchase details.",
  },
  {
    id: 4,
    title: "Review and predict",
    caption: "Check the summary, then generate the prediction.",
  },
];

const syncedModelDefaults = {
  basic: {
    ac_usage_level: "4",
    charging_type: "fast-dominant",
  },
  research: {
    ac_usage_level: "4",
    charging_type: "fast-dominant",
  },
};

const featureMetadata = {
  monthly_savings_rs: {
    label: "Monthly savings estimate",
    description: "Difference between yearly fuel cost and EV cost, converted into a monthly amount.",
  },
  total_annual_savings_rs: {
    label: "Total annual savings",
    description: "Combined yearly savings from lower energy cost and lower maintenance cost.",
  },
  maintenance_savings_rs_per_year: {
    label: "Maintenance savings per year",
    description: "How much maintenance cost is reduced after shifting from fuel to EV.",
  },
  electricity_price_per_kwh: {
    label: "Electricity price",
    description: "Power tariff used to estimate EV charging cost.",
  },
  ev_cost_rs_per_year: {
    label: "Estimated EV running cost",
    description: "Expected yearly EV energy cost based on usage and electricity price.",
  },
  eco_score: {
    label: "Eco score",
    description: "Environmental score derived from expected carbon reduction.",
  },
  annual_maintenance_cost_ev_rs: {
    label: "EV maintenance cost",
    description: "Yearly servicing and maintenance cost assumed for the EV.",
  },
  annual_maintenance_cost_fuel_rs: {
    label: "Fuel vehicle maintenance cost",
    description: "Yearly servicing and maintenance cost assumed for the fuel vehicle.",
  },
  subsidy_amount_rs: {
    label: "EV subsidy amount",
    description: "Government or purchase incentive considered in the EV ownership cost.",
  },
  battery_degradation_rate: {
    label: "Battery degradation rate",
    description: "Estimated battery wear over time using battery health and vehicle age.",
  },
};

const currencyFormatter = new Intl.NumberFormat("en-IN", {
  maximumFractionDigits: 0,
});

const metricFormatter = new Intl.NumberFormat("en-IN", {
  maximumFractionDigits: 2,
});

function formatCurrency(value) {
  return `Rs ${currencyFormatter.format(Number(value || 0))}`;
}

function formatMetric(value, unit = "") {
  return `${metricFormatter.format(Number(value || 0))}${unit ? ` ${unit}` : ""}`;
}

function getFeatureDetails(feature) {
  return (
    featureMetadata[feature] || {
      label: feature
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" "),
      description: "This is one of the model inputs or derived signals used during prediction.",
    }
  );
}

function formatImpact(value) {
  const numeric = Number(value || 0);
  return metricFormatter.format(Math.abs(numeric));
}

function getImpactSummary(value, kind) {
  const numeric = Number(value || 0);

  if (kind === "cost") {
    return numeric >= 0 ? "Increased predicted savings" : "Reduced predicted savings";
  }

  return numeric >= 0 ? "Increased carbon benefit" : "Reduced carbon benefit";
}

function Field({ label, hint, children }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {children}
      {hint ? <span className="field-hint">{hint}</span> : null}
    </label>
  );
}

function SummaryRow({ label, value }) {
  return (
    <div className="summary-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function FeatureInsight({ item, kind }) {
  const details = getFeatureDetails(item.feature);
  const numericImpact = Number(item.impact || 0);

  return (
    <li className="feature-item">
      <div className="feature-item-head">
        <div className="feature-copy">
          <strong>{details.label}</strong>
          <span className={`impact-chip ${numericImpact >= 0 ? "positive" : "negative"}`}>
            {getImpactSummary(numericImpact, kind)}
          </span>
        </div>
        <div className={`impact-number ${numericImpact >= 0 ? "positive" : "negative"}`}>
          <span className="impact-sign">{numericImpact >= 0 ? "+" : "-"}</span>
          <strong>{formatImpact(numericImpact)}</strong>
        </div>
      </div>
      <p>{details.description}</p>
    </li>
  );
}

export default function App() {
  const [modelType, setModelType] = useState("basic");
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState(defaultFormData);

  const quickStats = useMemo(
    () => ({
      annualDistance: formData.distance_km_per_day * formData.trip_days_per_year,
      yearlyFuelCost:
        (formData.distance_km_per_day * formData.trip_days_per_year) /
        Math.max(formData.fuel_vehicle_mileage_kmpl, 0.001) *
        formData.fuel_price_per_liter,
      yearlyEvCost:
        formData.distance_km_per_day *
        formData.trip_days_per_year *
        formData.ev_efficiency_kwh_per_km *
        formData.electricity_price_per_kwh,
    }),
    [formData]
  );

  const barData = result
    ? [
        { name: "Fuel Cost", value: result.fuel_cost_rs_per_year || 0 },
        { name: "EV Cost", value: result.ev_cost_rs_per_year || 0 },
        { name: "Savings", value: result.predicted_cost_savings_rs_per_year || 0 },
        { name: "Carbon Reduction", value: result.predicted_carbon_reduction_kg_per_year || 0 },
      ]
    : [];

  const lineData = result
    ? Array.from({ length: 5 }, (_, index) => ({
        year: `Year ${index + 1}`,
        savings: (result.predicted_cost_savings_rs_per_year || 0) * (index + 1),
      }))
    : [];

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: numberFields.has(name) ? Number(value) : value,
    }));
  };

  const handleModelSelect = (nextModelType) => {
    setModelType(nextModelType);
    setFormData((prev) => ({
      ...prev,
      ...syncedModelDefaults[nextModelType],
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const endpoint = `${API_BASE_URL}/predict/${modelType}`;
      const response = await axios.post(endpoint, formData);
      setResult(response.data);
      setCurrentStep(4);
    } catch (err) {
      setError(err?.response?.data?.detail || "Prediction failed. Check backend and input values.");
    } finally {
      setLoading(false);
    }
  };

  const goNext = () => setCurrentStep((step) => Math.min(step + 1, steps.length - 1));
  const goBack = () => setCurrentStep((step) => Math.max(step - 1, 0));

  const renderStep = () => {
    if (currentStep === 0) {
      return (
        <div className="step-layout">
          <section className="panel panel-hero">
            <p className="eyebrow">GreenVolt EV Predictor</p>
            <h1>Choose what you want to calculate.</h1>
            <p className="hero-copy">
              Instead of showing every field at once, this flow collects inputs in smaller pages and
              then sends them to your ML model.
            </p>

            <div className="choice-grid">
              <button
                type="button"
                className={`choice-card ${modelType === "basic" ? "selected" : ""}`}
                onClick={() => handleModelSelect("basic")}
              >
                <span className="choice-state">{modelType === "basic" ? "Selected model" : "Click to select"}</span>
                <span className="choice-kicker">Quick estimate</span>
                <strong>Basic model</strong>
                <span>Faster summary for cost savings and carbon reduction.</span>
              </button>

              <button
                type="button"
                className={`choice-card ${modelType === "research" ? "selected" : ""}`}
                onClick={() => handleModelSelect("research")}
              >
                <span className="choice-state">
                  {modelType === "research" ? "Selected model" : "Click to select"}
                </span>
                <span className="choice-kicker">Detailed analysis</span>
                <strong>Research model</strong>
                <span>Includes EV benefit, risk, economy, and environment scores.</span>
              </button>
            </div>
          </section>

          <aside className="panel panel-side">
            <h2>What this flow asks</h2>
            <div className="selected-model-banner">
              Selected: <strong>{modelType === "basic" ? "Basic model" : "Research model"}</strong>
            </div>
            <ul className="plain-list">
              <li>Travel details</li>
              <li>Charging and battery details</li>
              <li>Ownership and cost details</li>
              <li>Prediction summary on the final page</li>
            </ul>

            <div className="mini-summary">
              <SummaryRow label="Vehicle type" value={formData.vehicle_type} />
              <SummaryRow label="Daily distance" value={formatMetric(formData.distance_km_per_day, "km")} />
              <SummaryRow label="Annual distance" value={formatMetric(quickStats.annualDistance, "km")} />
            </div>
          </aside>
        </div>
      );
    }

    if (currentStep === 1) {
      return (
        <div className="step-layout">
          <section className="panel">
            <h2>Travel profile</h2>
            <p className="section-copy">Fill only the vehicle and daily usage inputs needed for the prediction.</p>

            <div className="field-grid">
              <Field label="Vehicle type">
                <select name="vehicle_type" value={formData.vehicle_type} onChange={handleChange}>
                  <option value="2-wheeler">2-wheeler</option>
                  <option value="4-wheeler">4-wheeler</option>
                </select>
              </Field>

              <Field label="Fuel type">
                <select name="fuel_type" value={formData.fuel_type} onChange={handleChange}>
                  <option value="petrol">Petrol</option>
                  <option value="diesel">Diesel</option>
                </select>
              </Field>

              <Field label="Distance per day" hint="Average travel in kilometers">
                <input
                  type="number"
                  min="1"
                  name="distance_km_per_day"
                  value={formData.distance_km_per_day}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Trip days per year">
                <input
                  type="number"
                  min="1"
                  max="365"
                  name="trip_days_per_year"
                  value={formData.trip_days_per_year}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Vehicle age">
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  name="vehicle_age_years"
                  value={formData.vehicle_age_years}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Fuel mileage">
                <input
                  type="number"
                  min="1"
                  step="0.1"
                  name="fuel_vehicle_mileage_kmpl"
                  value={formData.fuel_vehicle_mileage_kmpl}
                  onChange={handleChange}
                />
              </Field>

              <Field label="City traffic">
                <select name="city_traffic_level" value={formData.city_traffic_level} onChange={handleChange}>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </Field>

              <Field label="AC usage">
                <select name="ac_usage_level" value={formData.ac_usage_level} onChange={handleChange}>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                </select>
              </Field>

              <Field label="Highway ratio" hint="Value between 0 and 1">
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  name="highway_ratio"
                  value={formData.highway_ratio}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Urban ratio" hint="Value between 0 and 1">
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  name="urban_ratio"
                  value={formData.urban_ratio}
                  onChange={handleChange}
                />
              </Field>
            </div>
          </section>

          <aside className="panel panel-side">
            <h3>Live estimate</h3>
            <div className="mini-summary">
              <SummaryRow label="Annual distance" value={formatMetric(quickStats.annualDistance, "km")} />
              <SummaryRow label="Fuel type" value={formData.fuel_type} />
              <SummaryRow label="Route mix" value={`${formData.highway_ratio}/${formData.urban_ratio}`} />
            </div>
          </aside>
        </div>
      );
    }

    if (currentStep === 2) {
      return (
        <div className="step-layout">
          <section className="panel">
            <h2>Charging and energy</h2>
            <p className="section-copy">These inputs affect EV efficiency, battery behavior, and emissions.</p>

            <div className="field-grid">
              <Field label="EV efficiency">
                <input
                  type="number"
                  min="0.01"
                  step="0.01"
                  name="ev_efficiency_kwh_per_km"
                  value={formData.ev_efficiency_kwh_per_km}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Electricity price">
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  name="electricity_price_per_kwh"
                  value={formData.electricity_price_per_kwh}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Grid emission factor">
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  name="grid_emission_factor"
                  value={formData.grid_emission_factor}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Fuel emission factor">
                <input
                  type="number"
                  min="0"
                  step="0.01"
                  name="fuel_emission_factor"
                  value={formData.fuel_emission_factor}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Battery health">
                <input
                  type="number"
                  min="1"
                  max="100"
                  step="1"
                  name="battery_health_percent"
                  value={formData.battery_health_percent}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Battery capacity">
                <input
                  type="number"
                  min="1"
                  step="1"
                  name="battery_capacity_kwh"
                  value={formData.battery_capacity_kwh}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Home charging ratio">
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  name="home_charging_ratio"
                  value={formData.home_charging_ratio}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Public charging ratio">
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  name="public_charging_ratio"
                  value={formData.public_charging_ratio}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Fast charging ratio">
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  name="fast_charging_ratio"
                  value={formData.fast_charging_ratio}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Charging type">
                <select name="charging_type" value={formData.charging_type} onChange={handleChange}>
                  <option value="fast-dominant">Fast-dominant</option>
                  <option value="home/slow-dominant">Home/slow-dominant</option>
                  <option value="mixed">Mixed</option>
                </select>
              </Field>

              <Field label="Renewable energy ratio">
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  name="renewable_energy_usage_ratio"
                  value={formData.renewable_energy_usage_ratio}
                  onChange={handleChange}
                />
              </Field>
            </div>
          </section>

          <aside className="panel panel-side">
            <h3>Energy snapshot</h3>
            <div className="mini-summary">
              <SummaryRow label="Estimated EV cost/year" value={formatCurrency(quickStats.yearlyEvCost)} />
              <SummaryRow label="Battery health" value={formatMetric(formData.battery_health_percent, "%")} />
              <SummaryRow label="Charging type" value={formData.charging_type} />
            </div>
          </aside>
        </div>
      );
    }

    if (currentStep === 3) {
      return (
        <div className="step-layout">
          <section className="panel">
            <h2>Costs and ownership</h2>
            <p className="section-copy">This page captures fuel, maintenance, subsidy, and purchase values.</p>

            <div className="field-grid">
              <Field label="Fuel price per liter">
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  name="fuel_price_per_liter"
                  value={formData.fuel_price_per_liter}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Fuel vehicle purchase cost">
                <input
                  type="number"
                  min="0"
                  step="1000"
                  name="vehicle_purchase_cost_fuel_rs"
                  value={formData.vehicle_purchase_cost_fuel_rs}
                  onChange={handleChange}
                />
              </Field>

              <Field label="EV purchase cost">
                <input
                  type="number"
                  min="0"
                  step="1000"
                  name="vehicle_purchase_cost_ev_rs"
                  value={formData.vehicle_purchase_cost_ev_rs}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Fuel maintenance cost/year">
                <input
                  type="number"
                  min="0"
                  step="100"
                  name="annual_maintenance_cost_fuel_rs"
                  value={formData.annual_maintenance_cost_fuel_rs}
                  onChange={handleChange}
                />
              </Field>

              <Field label="EV maintenance cost/year">
                <input
                  type="number"
                  min="0"
                  step="100"
                  name="annual_maintenance_cost_ev_rs"
                  value={formData.annual_maintenance_cost_ev_rs}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Subsidy amount">
                <input
                  type="number"
                  min="0"
                  step="1000"
                  name="subsidy_amount_rs"
                  value={formData.subsidy_amount_rs}
                  onChange={handleChange}
                />
              </Field>

              <Field label="Road tax savings">
                <input
                  type="number"
                  min="0"
                  step="1000"
                  name="road_tax_savings_rs"
                  value={formData.road_tax_savings_rs}
                  onChange={handleChange}
                />
              </Field>
            </div>
          </section>

          <aside className="panel panel-side">
            <h3>Ownership snapshot</h3>
            <div className="mini-summary">
              <SummaryRow label="Estimated fuel cost/year" value={formatCurrency(quickStats.yearlyFuelCost)} />
              <SummaryRow
                label="Maintenance gap"
                value={formatCurrency(
                  formData.annual_maintenance_cost_fuel_rs - formData.annual_maintenance_cost_ev_rs
                )}
              />
              <SummaryRow
                label="Price difference"
                value={formatCurrency(formData.vehicle_purchase_cost_ev_rs - formData.vehicle_purchase_cost_fuel_rs)}
              />
            </div>
          </aside>
        </div>
      );
    }

    return (
      <div className="step-layout">
        <section className="panel">
          <h2>Review and predict</h2>
          <p className="section-copy">
            Everything is grouped here before sending the request to the {modelType} ML model.
          </p>

          <div className="review-grid">
            <div className="review-card">
              <h3>Travel</h3>
              <SummaryRow label="Vehicle" value={`${formData.vehicle_type} • ${formData.fuel_type}`} />
              <SummaryRow label="Distance/day" value={formatMetric(formData.distance_km_per_day, "km")} />
              <SummaryRow label="Trip days/year" value={formatMetric(formData.trip_days_per_year)} />
              <SummaryRow label="Annual distance" value={formatMetric(quickStats.annualDistance, "km")} />
            </div>

            <div className="review-card">
              <h3>Charging</h3>
              <SummaryRow label="EV efficiency" value={formatMetric(formData.ev_efficiency_kwh_per_km, "kWh/km")} />
              <SummaryRow label="Battery health" value={formatMetric(formData.battery_health_percent, "%")} />
              <SummaryRow label="Home/Public" value={`${formData.home_charging_ratio} / ${formData.public_charging_ratio}`} />
              <SummaryRow label="Charging type" value={formData.charging_type} />
            </div>

            <div className="review-card">
              <h3>Cost</h3>
              <SummaryRow label="Fuel price" value={formatCurrency(formData.fuel_price_per_liter)} />
              <SummaryRow label="Fuel cost/year" value={formatCurrency(quickStats.yearlyFuelCost)} />
              <SummaryRow label="EV cost/year" value={formatCurrency(quickStats.yearlyEvCost)} />
              <SummaryRow label="Subsidy" value={formatCurrency(formData.subsidy_amount_rs)} />
            </div>
          </div>

          <button className="submit-btn" type="submit" disabled={loading}>
            {loading ? "Predicting..." : `Run ${modelType} prediction`}
          </button>
        </section>

        <aside className="panel panel-side">
          <h3>Selected model</h3>
          <p className="side-copy">
            {modelType === "basic"
              ? "The basic model gives the core savings and carbon result."
              : "The research model also returns EV benefit, risk, economic, and environment scores."}
          </p>
        </aside>
      </div>
    );
  };

  return (
    <div className="app-shell">
      <div className="background-orb background-orb-left" />
      <div className="background-orb background-orb-right" />

      <main className="app-frame">
        <section className="topbar">
          <div>
            <p className="eyebrow">Frontend redesign</p>
            <h1 className="app-title">GreenVolt EV Cost and Carbon Predictor</h1>
            <p className="subtitle">
              A cleaner step-by-step frontend for your existing ML model integration.
            </p>
          </div>

          <button
            type="button"
            className="ghost-btn"
            onClick={() => {
              setFormData(defaultFormData);
              setResult(null);
              setError("");
              setCurrentStep(0);
              handleModelSelect("basic");
            }}
          >
            Reset flow
          </button>
        </section>

        <section className="stepper">
          {steps.map((step) => (
            <button
              key={step.id}
              type="button"
              className={`step-pill ${currentStep === step.id ? "active" : ""} ${
                currentStep > step.id ? "complete" : ""
              }`}
              onClick={() => setCurrentStep(step.id)}
            >
              <span>{step.id + 1}</span>
              <strong>{step.title}</strong>
            </button>
          ))}
        </section>

        <section className="section-header">
          <div>
            <h2>{steps[currentStep].title}</h2>
            <p>{steps[currentStep].caption}</p>
          </div>
          <div className="section-meta">
            <div className="model-chip">{modelType === "basic" ? "Basic model" : "Research model"}</div>
            <div className="progress-chip">
              Step {currentStep + 1} of {steps.length}
            </div>
          </div>
        </section>

        <form onSubmit={handleSubmit}>
          {renderStep()}

          <div className="nav-row">
            <button type="button" className="ghost-btn" onClick={goBack} disabled={currentStep === 0 || loading}>
              Back
            </button>

            {currentStep < steps.length - 1 ? (
              <button type="button" className="primary-btn" onClick={goNext}>
                Next
              </button>
            ) : null}
          </div>
        </form>

        {error ? <div className="error-box">{error}</div> : null}

        {result && currentStep === steps.length - 1 ? (
          <section className="results-section">
            <div className="results-header">
              <div>
                <p className="eyebrow">Prediction result</p>
                <h2>Model output</h2>
              </div>
              <span className="result-badge">{result.model_type} model</span>
            </div>

            <div className="cards">
              <div className="card accent-card">
                <h3>Predicted savings / year</h3>
                <p>{formatCurrency(result.predicted_cost_savings_rs_per_year)}</p>
              </div>
              <div className="card">
                <h3>Carbon reduction / year</h3>
                <p>{formatMetric(result.predicted_carbon_reduction_kg_per_year, "kg")}</p>
              </div>
              <div className="card">
                <h3>5-year savings</h3>
                <p>{formatCurrency(result.predicted_5yr_savings_rs)}</p>
              </div>
              <div className="card">
                <h3>Trees saved</h3>
                <p>{formatMetric(result.trees_saved_equivalent)}</p>
              </div>
              <div className="card">
                <h3>Fuel cost / year</h3>
                <p>{formatCurrency(result.fuel_cost_rs_per_year)}</p>
              </div>
              <div className="card">
                <h3>EV cost / year</h3>
                <p>{formatCurrency(result.ev_cost_rs_per_year)}</p>
              </div>
              {result.overall_ev_benefit_score !== undefined ? (
                <div className="card">
                  <h3>Overall EV benefit</h3>
                  <p>{formatMetric(result.overall_ev_benefit_score)}</p>
                </div>
              ) : null}
              {result.risk_score !== undefined ? (
                <div className="card">
                  <h3>Risk score</h3>
                  <p>{formatMetric(result.risk_score)}</p>
                </div>
              ) : null}
              {result.economic_score !== undefined ? (
                <div className="card">
                  <h3>Economic score</h3>
                  <p>{formatMetric(result.economic_score)}</p>
                </div>
              ) : null}
              {result.environment_score !== undefined ? (
                <div className="card">
                  <h3>Environment score</h3>
                  <p>{formatMetric(result.environment_score)}</p>
                </div>
              ) : null}
            </div>

            <div className="results-grid">
              <div className="chart-box">
                <h3>Cost and carbon comparison</h3>
                <ResponsiveContainer width="100%" height={320}>
                  <BarChart data={barData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#2f855a" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-box">
                <h3>5-year savings trend</h3>
                <ResponsiveContainer width="100%" height={320}>
                  <LineChart data={lineData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="savings" stroke="#c05621" strokeWidth={3} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {result.chart_url ? (
              <div className="chart-box">
                <h3>Backend-generated chart</h3>
                <img
                  src={`${API_BASE_URL}${result.chart_url}`}
                  alt="Prediction chart"
                  className="backend-chart"
                />
              </div>
            ) : null}

            <div className="results-grid">
              {result.top_cost_features?.length ? (
                <div className="feature-box">
                  <h3>What most affected cost prediction</h3>
                  <ul className="feature-list">
                    {result.top_cost_features.map((item) => (
                      <FeatureInsight key={`cost-${item.feature}`} item={item} kind="cost" />
                    ))}
                  </ul>
                </div>
              ) : null}

              {result.top_carbon_features?.length ? (
                <div className="feature-box">
                  <h3>What most affected carbon prediction</h3>
                  <ul className="feature-list">
                    {result.top_carbon_features.map((item) => (
                      <FeatureInsight key={`carbon-${item.feature}`} item={item} kind="carbon" />
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          </section>
        ) : null}
      </main>
    </div>
  );
}
