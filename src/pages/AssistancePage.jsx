import { motion } from "framer-motion";
import { Link } from "react-router-dom";

export default function AssistancePage() {
  return (
    <div className="assistance-page">

      {/* HEADER LOCAL */}
      <header className="header">
        <div className="header-inner">
          <Link to="/" className="logo-area">
            <div className="logo-icon">A</div>
            <div className="logo-text">
              <span className="brand">HackaPrint</span>
              <span className="tagline">Service d'assistance</span>
            </div>
          </Link>
        </div>
      </header>

      {/* HERO */}
      <section className="section section-alt">
        <motion.div
          className="section-header"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2>Besoins d’aide ?</h2>
          <p>Contactez-nous via le canal qui vous convient le mieux.</p>
        </motion.div>
      </section>

      {/* CONTACT OPTIONS */}
      <section className="section">
        <div className="contact-grid">

          {/* TELEPHONE */}
          <motion.div
            className="contact-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h3>📞 Assistance Téléphonique</h3>
            <p>Disponible 7j/7 - 24h/24</p>
            <div className="contact-info">
              <strong>+33 1 84 60 24 90</strong>
            </div>
            <button className="btn primary full">Appeler maintenant</button>
          </motion.div>

          {/* EMAIL */}
          <motion.div
            className="contact-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h3>📧 Assistance par E-mail</h3>
            <p>Réponse à votre demande immédiatement.</p>
            <div className="contact-info">
              <strong>support@hackprint.com</strong>
            </div>
            <button className="btn secondary full">Envoyer un e-mail</button>
          </motion.div>

          {/* SMS */}
          <motion.div
            className="contact-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h3>💬 Assistance SMS</h3>
            <p>Résolution rapide, directement sur votre téléphone.</p>
            <div className="contact-info">
              <strong>06 55 44 33 22</strong>
            </div>
            <button className="btn ghost full">Envoyer un SMS</button>
          </motion.div>

        </div>
      </section>

      {/* FUTURE TICKET SYSTEM */}
      <section className="section section-alt">
        <motion.div
          className="ticket-card"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <h3>🎟 Créer un ticket (bientôt)</h3>
          <p>Un système complet d'assistance automatisée sera bientôt disponible.</p>
          <button className="btn ghost">Système en cours d’intégration…</button>
        </motion.div>
      </section>
    </div>
  );
}
