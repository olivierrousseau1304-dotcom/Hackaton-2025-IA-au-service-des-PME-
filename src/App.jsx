import React from "react";
import { motion } from "framer-motion";
import { Routes, Route, Link } from "react-router-dom";
import AssistancePage from "./pages/AssistancePage.jsx";

// --- Données ---
const printers = [
  {
    name: "HackaPrint X500",
    type: "Imprimante laser couleur",
    description:
      "Idéale pour les petites entreprises : rapide, silencieuse, avec Wi-Fi et impression recto-verso automatique.",
    price: "349,00 €",
    badge: "Nouveau",
  },
  {
    name: "HackaPrint HomeJet 210",
    type: "Imprimante jet d’encre",
    description:
      "Parfaite pour la maison : impression de photos, documents scolaires et numérisation vers le cloud.",
    price: "129,00 €",
    badge: "Meilleure vente",
  },
  {
    name: "HackaPrint ProOffice 900",
    type: "Multifonction 4-en-1",
    description:
      "Copie, scan, fax et impression haute capacité. Conçue pour les environnements de bureau exigeants.",
    price: "599,00 €",
    badge: "Pro",
  },
];

const supportCards = [
  {
    title: "Guides d’installation",
    description:
      "Suivez pas à pas l’installation de votre imprimante, du déballage à la première page imprimée.",
    action: "Voir les guides",
  },
  {
    title: "Pilotes & logiciels",
    description:
      "Téléchargez la dernière version des pilotes, utilitaires et firmwares pour votre modèle.",
    action: "Accéder aux pilotes",
  },
  {
    title: "Centre d’aide",
    description:
      "Questions fréquentes, résolution de pannes et astuces pour une impression sans stress.",
    action: "Visiter l’aide",
  },
];

const faqs = [
  {
    question: "Comment installer mon imprimante pour la première fois ?",
    answer:
      "Branchez l’imprimante, installez les cartouches, chargez le papier, puis lancez l’assistant d’installation via le pilote ou l’application mobile HackaPrint Connect.",
  },
  {
    question: "Où trouver les pilotes compatibles avec mon système ?",
    answer:
      "Rendez-vous dans la section Téléchargements, sélectionnez votre modèle et votre système d’exploitation.",
  },
  {
    question: "Pourquoi mon imprimante n’apparaît pas sur le réseau Wi-Fi ?",
    answer:
      "Vérifiez que le Wi-Fi est activé sur l’imprimante, que vous êtes sur la bonne bande (2.4 GHz), et redémarrez votre box.",
  },
];

// Animation
const fadeInUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (delay = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay },
  }),
};

// ------------------------------------------------------
// ROUTER PRINCIPAL
// ------------------------------------------------------
function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/assistance" element={<AssistancePage />} />
    </Routes>
  );
}

// ------------------------------------------------------
// PAGE D’ACCUEIL
// ------------------------------------------------------
function HomePage() {
  return (
    <div className="page">
      {/* HEADER */}
      <header className="header">
        <motion.div
          className="header-inner"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="logo-area">
            <div className="logo-icon">A</div>
            <div className="logo-text">
              <span className="brand">HackaPrint</span>
              <span className="tagline">Imprimez sans limite</span>
            </div>
          </div>

          <nav className="nav">
            <a href="#products">Produits</a>
            <Link to="/assistance">Assistance</Link>
            <a href="#downloads">Téléchargements</a>
            <a href="#faq">FAQ</a>
          </nav>

          <div className="header-actions">
            <button className="btn ghost">Se connecter</button>
            <button className="btn primary">Créer un compte</button>
          </div>
        </motion.div>
      </header>

      {/* ------------------ HERO ------------------ */}
      <main>
        <section className="hero">
          <div className="hero-inner">
            <motion.div
              className="hero-text"
              initial="hidden"
              animate="visible"
              variants={fadeInUp}
              custom={0}
            >
              <h1>
                Une nouvelle génération
                <br />
                d&apos;imprimantes intelligentes.
              </h1>

              <p>
                Connectez, imprimez, scannez et gérez votre parc en toute simplicité.
              </p>

              <div className="hero-actions">
                <button className="btn primary large">
                  Découvrir la gamme
                </button>

                <Link to="/assistance" className="btn ghost large">
                  Contacter l&apos;assistance
                </Link>
              </div>

              <p className="hero-subtext">
                ✔ Installation guidée • ✔ Mise à jour automatique • ✔ Assistance 7j/7
              </p>
            </motion.div>

            <motion.div
              className="hero-card"
              initial={{ opacity: 0, scale: 0.9, x: 40 }}
              animate={{ opacity: 1, scale: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div className="printer-visual">
                <div className="printer-top" />
                <div className="printer-body" />
                <div className="printer-paper" />
              </div>

              <div className="hero-card-content">
                <h2>HackaPrint X500</h2>
                <p>Jusqu'à 32 pages/minute, Wi-Fi 6.</p>

                <ul className="hero-specs">
                  <li>Wi-Fi • USB • Ethernet</li>
                  <li>2400 x 1200 dpi</li>
                  <li>App mobile HackaPrint</li>
                </ul>

                <button className="btn secondary full">
                  Voir les détails techniques
                </button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* ------------------ PRODUITS ------------------ */}
        <section id="products" className="section">
          <motion.div
            className="section-header"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={fadeInUp}
            custom={0}
          >
            <h2>Notre gamme d&apos;imprimantes</h2>
            <p>
              Une solution adaptée à chaque besoin, de la maison au bureau.
            </p>
          </motion.div>

          <div className="cards-grid">
            {printers.map((printer, index) => (
              <motion.article
                key={printer.name}
                className="card product-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                whileHover={{ y: -6, scale: 1.01 }}
              >
                <div className="card-badge">{printer.badge}</div>
                <h3>{printer.name}</h3>
                <p className="product-type">{printer.type}</p>
                <p className="product-description">{printer.description}</p>

                <div className="product-footer">
                  <span className="price">{printer.price}</span>
                  <button className="btn ghost small">Voir ce modèle</button>
                </div>
              </motion.article>
            ))}
          </div>
        </section>

        {/* ------------------ ASSISTANCE ------------------ */}
        <section id="support" className="section section-alt">
          <motion.div
            className="section-header"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={fadeInUp}
          >
            <h2>Assistance HackaPrint</h2>
            <p>
              Installation, mises à jour, problèmes… notre équipe vous accompagne.
            </p>
          </motion.div>

          <div className="support-layout">
            <div className="support-cards">
              {supportCards.map((card, index) => (
                <motion.div
                  key={card.title}
                  className="card support-card"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.2 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  whileHover={{ y: -4 }}
                >
                  <h3>{card.title}</h3>
                  <p>{card.description}</p>
                  <button className="link-button">{card.action} →</button>
                </motion.div>
              ))}
            </div>

            <motion.div
              className="support-panel"
              initial={{ opacity: 0, x: 40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.5 }}
            >
              <h3>Besoin d&apos;aide immédiate ?</h3>
              <p>Décrivez votre problème et nous vous proposerons les solutions adaptées.</p>

              <form
                className="support-form"
                onSubmit={(e) => {
                  e.preventDefault();
                  alert("Démo : aucun message n'est envoyé 😄");
                }}
              >
                <label>
                  Sélectionnez votre produit
                  <select required>
                    <option value="">Choisissez un modèle</option>
                    <option>HackaPrint X500</option>
                    <option>HackaPrint HomeJet 210</option>
                    <option>HackaPrint ProOffice 900</option>
                    <option>Autre modèle</option>
                  </select>
                </label>

                <label>
                  Décrivez votre problème
                  <textarea
                    rows="3"
                    placeholder="Ex : Mon imprimante n'apparaît pas sur le réseau Wi-Fi."
                    required
                  />
                </label>

                <button type="submit" className="btn primary full">
                  Obtenir de l&apos;aide
                </button>
              </form>
            </motion.div>
          </div>
        </section>

        {/* ------------------ DOWNLOADS ------------------ */}
        <section id="downloads" className="section">
          <motion.div
            className="section-header"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={fadeInUp}
          >
            <h2>Pilotes & téléchargements</h2>
            <p>Mettez vos imprimantes à jour avec les derniers pilotes disponibles.</p>
          </motion.div>

          <motion.div
            className="downloads-panel"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
          >
            <form
              className="downloads-form"
              onSubmit={(e) => {
                e.preventDefault();
                alert("Démo : recherche fictive !");
              }}
            >
              <div className="form-row">
                <label>
                  Modèle d&apos;imprimante
                  <input type="text" placeholder="Ex : HackaPrint X500" required />
                </label>

                <label>
                  Système d&apos;exploitation
                  <select required>
                    <option value="">Choisissez…</option>
                    <option>Windows 11</option>
                    <option>Windows 10</option>
                    <option>macOS (Apple Silicon)</option>
                    <option>macOS (Intel)</option>
                    <option>Linux</option>
                  </select>
                </label>
              </div>

              <button type="submit" className="btn secondary full">
                Rechercher les pilotes
              </button>
            </form>
          </motion.div>
        </section>

        {/* ------------------ FAQ ------------------ */}
        <section id="faq" className="section section-alt">
          <motion.div
            className="section-header"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={fadeInUp}
          >
            <h2>Questions fréquentes</h2>
          </motion.div>

          <div className="faq-list">
            {faqs.map((item, index) => (
              <motion.details
                key={item.question}
                className="faq-item"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <summary>{item.question}</summary>
                <p>{item.answer}</p>
              </motion.details>
            ))}
          </div>
        </section>

        {/* ------------------ NEWSLETTER ------------------ */}
        <section className="section newsletter-section">
          <motion.div
            className="newsletter-card"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.4 }}
          >
            <h2>Restez informé(e)</h2>
            <p>Recevez nos actualités et astuces par e-mail.</p>

            <form
              className="newsletter-form"
              onSubmit={(e) => {
                e.preventDefault();
                alert("Merci ! (démonstration)");
              }}
            >
              <input type="email" placeholder="Votre adresse e-mail" required />
              <button type="submit" className="btn primary">
                S&apos;abonner
              </button>
            </form>
          </motion.div>
        </section>
      </main>

      {/* ------------------ FOOTER ------------------ */}
      <footer className="footer">
        <div className="footer-inner">
          <div>
            <h3>HackaPrint</h3>
            <p>Interface moderne d’imprimantes intelligentes — démonstration front-end.</p>
          </div>

          <div className="footer-columns">
            <div>
              <h4>Produits</h4>
              <ul>
                <li><a href="#products">Imprimantes</a></li>
                <li><a href="#downloads">Pilotes</a></li>
              </ul>
            </div>

            <div>
              <h4>Assistance</h4>
              <ul>
                <li><Link to="/assistance">Contact Support</Link></li>
                <li><a href="#faq">FAQ</a></li>
              </ul>
            </div>

            <div>
              <h4>Légal</h4>
              <ul>
                <li><a href="#">Mentions légales</a></li>
                <li><a href="#">Politique de confidentialité</a></li>
              </ul>
            </div>
          </div>
        </div>

        <p className="footer-bottom">
          © {new Date().getFullYear()} HackaPrint — Démonstration front-end.
        </p>
      </footer>
    </div>
  );
}

export default App;
