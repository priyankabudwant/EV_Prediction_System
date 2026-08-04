import React from "react";
import { motion } from "framer-motion";

const Navbar = () => {
  return (
    <motion.nav
      className="navbar"
      initial={{ y: -60, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="logo">⚡ EV Intelligence</div>
      <div className="nav-links">
        <a href="#growth">Growth</a>
        <a href="#top5">Top 5</a>
        <a href="#co2">CO₂</a>
      </div>
    </motion.nav>
  );
};

export default Navbar;
