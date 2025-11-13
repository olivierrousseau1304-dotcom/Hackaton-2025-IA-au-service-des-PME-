// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";



// Pages
import HomePage from "./HomePage.jsx";
import AssistancePage from "./pages/AssistancePage.jsx";
import AdminPage from "./pages/AdminPage.jsx";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/assistance" element={<AssistancePage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </Router>
  );
}
