# Automatisation intelligente du support client

Prototype pour un projet de hackathon : service de support client augmenté par l'IA (niveau 1 automatisé).

## 📋 Contenu du repo

- `setup_database.py` — Crée la base SQLite `support_client.db` depuis `tickets.json`
- `load_mysql.py` — Charge les données JSON dans une base MySQL
- `schema.sql` — Schéma complet MySQL (tables, index, vues, contraintes)
- `test_database.py` — Script simple pour vérifier la base SQLite et afficher des stats
- `tickets.json` — Dataset de 50 tickets d'exemple

## 🚀 Démarrage rapide (SQLite local)

### 1. Installer Python 3.8+

```bash
python3 --version
```

### 2. Créer un environnement virtuel (optionnel)

```bash
python3 -m venv .venv
source .venv/bin/activate  # sur Linux/Mac
# ou
.venv\Scripts\activate  # sur Windows
```

### 3. Initialiser la base et peupler les données

```bash
python3 setup_database.py
```

Résultat : `support_client.db` créée avec 48 clients, 5 résolutions et 50 tickets.

### 4. Vérifier la base

```bash
python3 test_database.py
```

## 🗄️ Déploiement MySQL (serveur)

### Prérequis

- MySQL 5.7+ installé et en cours d'exécution
- Python avec le connecteur MySQL (`pip install mysql-connector-python`)

### Étape 1 : Créer la base de données MySQL

```bash
mysql -u root -p
```

Puis exécuter en MySQL :

```sql
CREATE DATABASE support_client CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Étape 2 : Importer le schéma

```bash
mysql -u root -p support_client < schema.sql
```

Cela crée toutes les tables, index et vues.

### Étape 3 : Charger les données

```bash
pip install mysql-connector-python
python3 load_mysql.py --database support_client --user root --password votre_mot_de_passe
```

Options du script `load_mysql.py` :

```bash
python3 load_mysql.py \
  --host localhost \
  --user root \
  --password votre_mot_de_passe \
  --database support_client \
  --json-file tickets.json
```

### Étape 4 : Vérifier les données

```bash
mysql -u root -p support_client -e "SELECT COUNT(*) as total_tickets FROM tickets;"
```

Résultat attendu : 50 tickets

## 📊 Tables disponibles

- **clients** — Informations clients (id, nom, email, licence, niveau technique)
- **tickets** — Tickets de support (id, sujet, catégorie, statut, confiance, résolution)
- **resolutions** — Base de connaissance (KB entries avec étapes et taux réussite)
- **ticket_history** — Historique des actions par ticket (audit)
- **automation_metrics** — Métriques d'automatisation par jour

## 🔍 Vues SQL disponibles

- **v_unresolved_tickets** — Tickets non résolus triés par priorité
- **v_automation_performance** — Taux d'automatisation par jour

## 🏗️ Prochaines étapes recommandées

- [ ] Ajouter une API REST (FastAPI/Flask) pour ingestion et décision IA
- [ ] Implémenter un modèle ML (classificateur NLP) pour scoring automatique
- [ ] Créer un orchestrateur d'auto-résolution avec logging
- [ ] Ajouter des métriques et monitoring (Prometheus/Grafana optionnel)
- [ ] Tests unitaires et CI/CD

## 📝 Structure des données JSON (tickets.json)

Chaque ticket contient :

```json
{
  "ticket_id": "TK001",
  "channel": "email",
  "client_id": "CL001",
  "timestamp": "2025-01-15T09:23:00Z",
  "subject": "Impossible de se connecter à Outlook",
  "content": "...",
  "category": "authentification",
  "subcategory": "outlook_login",
  "priority": "high",
  "auto_resolvable": true,
  "resolution_type": "reset_password",
  "estimated_resolution_time": "5min",
  "knowledge_base_ref": "KB-AUTH-001"
}
```

## 🔐 Sécurité

- Données sensibles (PII) : sans chiffrement en local/dev, à ajouter en production
- Connexion MySQL : utiliser des variables d'environnement pour les credentials
- Accès BD : limiter les droits MySQL par utilisateur (read/write/admin)

## 📄 Licence

MIT

## 👥 Groupe / Auteurs

Projet Hackathon 2025 — IA au service des PME
