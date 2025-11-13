import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export default function Header({ admin = false }) {
  return (
    <header className="header">
      <motion.div
        className="header-inner"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <Link to="/" className="logo-area">
          <div className="logo-icon">A</div>
          <div className="logo-text">
            <span className="brand">HackaPrint</span>
            <span className="tagline">
              {admin ? "Espace Admin" : "Imprimez sans limite"}
            </span>
          </div>
        </Link>

        <nav className="nav">
          <Link to="/">Accueil</Link>
          <Link to="/assistance">Assistance</Link>
          <Link to="/admin">Admin</Link>
        </nav>

        <div className="header-actions">
          <button className="btn ghost">
            {admin ? "Se déconnecter" : "Se connecter"}
          </button>
        </div>
      </motion.div>
    </header>
  );
}
