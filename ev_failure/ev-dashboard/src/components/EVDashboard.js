import React, { useState } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

const COLORS = ["#00ff9f", "#ff4d4d"];

export default function EVDashboard() {

  const [analysis, setAnalysis] = useState(null);

  const fetchAnalysis = async () => {
    const response = await axios.post("http://127.0.0.1:8000/vehicle-analysis?vehicle_id=1", {
      Battery_Temperature: 40,
      Motor_Temperature: 55,
      Motor_Vibration: 0.3,
      SoH: 0.82
    });

    setAnalysis(response.data);
  };

  const downloadPDF = () => {
    const input = document.getElementById("dashboard");

    html2canvas(input).then((canvas) => {
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF();

      pdf.addImage(imgData, "PNG", 10, 10, 180, 160);
      pdf.save("EV_Report.pdf");
    });
  };

  if (!analysis) {
    return (
      <div style={{textAlign:"center", marginTop:"100px"}}>
        <button onClick={fetchAnalysis}>Run Vehicle Analysis</button>
      </div>
    );
  }

  const gaugeData = [
    { name: "Risk", value: analysis.failure_probability * 100 },
    { name: "Safe", value: 100 - analysis.failure_probability * 100 }
  ];

  const trendData = Object.entries(analysis.trend_summary).map(([k,v]) => ({
    name: k,
    value: v
  }));

  return (

    <div id="dashboard" style={{background:"#0f172a",color:"white",padding:"30px"}}>

      <h1 style={{textAlign:"center"}}>⚡ EV Failure Prediction Dashboard</h1>

      {/* Failure Risk Gauge */}

      <div style={{display:"flex",justifyContent:"center"}}>

        <PieChart width={300} height={300}>
          <Pie
            data={gaugeData}
            cx="50%"
            cy="50%"
            innerRadius={70}
            outerRadius={100}
            dataKey="value"
          >
            {gaugeData.map((entry,index)=>(
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
        </PieChart>

      </div>

      <h2 style={{textAlign:"center"}}>
        Failure Risk: {(analysis.failure_probability*100).toFixed(2)}%
      </h2>

      {/* Vehicle Health Cards */}

      <div style={{
        display:"grid",
        gridTemplateColumns:"repeat(3,1fr)",
        gap:"20px",
        marginTop:"40px"
      }}>

        <div className="card">
          <h3>Battery Temperature</h3>
          <p>{analysis.trend_summary.Battery_Temperature}</p>
        </div>

        <div className="card">
          <h3>Motor Temperature</h3>
          <p>{analysis.trend_summary.Motor_Temperature}</p>
        </div>

        <div className="card">
          <h3>Motor Vibration</h3>
          <p>{analysis.trend_summary.Motor_Vibration}</p>
        </div>

      </div>

      {/* RUL */}

      <h2 style={{marginTop:"40px"}}>
        Remaining Useful Life: {analysis.predicted_rul_hours} Hours
      </h2>

      {/* Maintenance Cost */}

      <h2>Maintenance Cost</h2>

      <p>Cost Now: ₹{analysis.maintenance_cost_now}</p>
      <p>Cost If Delayed: ₹{analysis.maintenance_cost_if_delayed}</p>

      {/* Trend Chart */}

      <h2 style={{marginTop:"40px"}}>Vehicle Trend Analysis</h2>

      <LineChart width={600} height={300} data={trendData}>
        <CartesianGrid strokeDasharray="3 3"/>
        <XAxis dataKey="name"/>
        <YAxis/>
        <Tooltip/>
        <Line type="monotone" dataKey="value" stroke="#00ff9f"/>
      </LineChart>

      {/* Download Report */}

      <div style={{marginTop:"40px"}}>

        <button onClick={downloadPDF}>
          Download Vehicle Report
        </button>

      </div>

    </div>
  );
}