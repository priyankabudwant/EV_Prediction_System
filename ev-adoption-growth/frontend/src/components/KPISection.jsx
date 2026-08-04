import React from "react";
import { motion } from "framer-motion";

const KPISection = ({ top5Growth, co2Data }) => {
  const totalGrowth = top5Growth.reduce((a, b) => a + b.growth, 0);
  const totalCO2 = co2Data.reduce((a, b) => a + b.co2_reduction, 0);

  return (
    <div className="kpi-section">
      <motion.div className="kpi-card" whileHover={{ scale: 1.05 }}>
        <h3>Total Growth (Top 5)</h3>
        <p>{totalGrowth.toLocaleString()}</p>
      </motion.div>

      <motion.div className="kpi-card" whileHover={{ scale: 1.05 }}>
        <h3>Total CO₂ Reduction</h3>
        <p>{totalCO2.toLocaleString()} tons</p>
      </motion.div>

      <motion.div className="kpi-card" whileHover={{ scale: 1.05 }}>
        <h3>Top Category</h3>
        <p>{top5Growth[0]?.category}</p>
      </motion.div>
    </div>
  );
};

export default KPISection;
