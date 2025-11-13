import Header from "../components/Header";
import { motion } from "framer-motion";

const ticketsOpen = 12;
const ticketsToday = 4;
const avgResolution = "2h 15m";

export default function AdminPage() {
  return (
    <div className="admin-page">
      <Header admin />

      {/* ------------------ TITRE ------------------ */}
      <div className="section">
        <h1>Tableau de bord Administrateur</h1>
        <p>Gestion des tickets et statistiques générales.</p>
      </div>

      {/* ------------------ STATISTIQUES ------------------ */}
      <div className="admin-stats">
        <motion.div
          className="admin-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h3>Tickets en cours</h3>
          <p className="big-number">{ticketsOpen}</p>
        </motion.div>

        <motion.div
          className="admin-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <h3>Tickets créés aujourd'hui</h3>
          <p className="big-number">{ticketsToday}</p>
        </motion.div>

        <motion.div
          className="admin-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h3>Temps moyen de résolution</h3>
          <p className="big-number">{avgResolution}</p>
        </motion.div>
      </div>

      {/* ------------------ PLACEHOLDER POUR LES FUTURS GRAPHS ------------------ */}
      <motion.div
        className="admin-graph-placeholder"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <h3>Statistiques avancées</h3>
        <p className="graph-placeholder-text">
          📊 Graphiques & analytics seront intégrés ici plus tard.
        </p>
      </motion.div>
    </div>
  );
}
