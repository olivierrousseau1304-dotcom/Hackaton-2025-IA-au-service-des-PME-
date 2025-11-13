import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function Header({ admin }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className={`header ${admin ? "header-admin" : ""}`}>
      <div className="header-inner">
        {/* LOGO */}
        <div className="logo-area">
          <div className="logo-icon">H</div>
          <div className="logo-text">
            <span className="brand">HackaPrint</span>
            <span className="tagline">Support & Drivers</span>
          </div>
        </div>

        {/* NAVIGATION (desktop) */}
        <nav className="nav">
          <Link to="/">Accueil</Link>
          <Link to="/assistance">Assistance</Link>
          <Link to="/admin">Admin</Link>
        </nav>

        {/* MENU BURGER (mobile only) */}
        <button
          className="burger"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <span></span><span></span><span></span>
        </button>
      </div>

      {/* MENU MOBILE */}
      {menuOpen && (
        <div className="mobile-menu">
          <Link to="/" onClick={() => setMenuOpen(false)}>Accueil</Link>
          <Link to="/assistance" onClick={() => setMenuOpen(false)}>Assistance</Link>
          <Link to="/admin" onClick={() => setMenuOpen(false)}>Admin</Link>
        </div>
      )}
    </header>
  );
}
