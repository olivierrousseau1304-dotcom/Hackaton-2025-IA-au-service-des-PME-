# Support Imprimantes Intelligent - Pipeline IA

Système de support automatisé pour PME vendant des imprimantes, avec pipeline IA complet : **Classification → Extraction → RAG → Réponse → Envoi multicanal**.

## 📋 Architecture du Projet

### Base de Données MySQL
- **15 tables principales** : `customers`, `printer_models`, `devices`, `knowledge_base`, `tickets`, `messages`, `attachments`, `extractions`, `rag_results`, `predictions`, `responses`, `outbound_logs`, `processing_steps`, `ticket_history`, `automation_metrics`
- **3 vues** : `v_actionable_tickets`, `v_pipeline_performance`, `v_unprocessed_messages`
- **Indexation FULLTEXT** pour recherche RAG dans la knowledge base

### API REST (FastAPI)
- Gestion tickets et clients
- Ingestion messages multicanaux (email, SMS, chat, appel)
- Recherche knowledge base (RAG)
- Monitoring pipeline IA
- **Port 8000** par défaut (configurable)

### Pipeline IA
1. **Ingestion** : Réception message (email/SMS/chat/call)
2. **Classification** : Catégorisation automatique (technique, commande, demande info)
3. **Extraction** : Extraction données structurées (modèle imprimante, code erreur, numéro série)
4. **RAG** : Recherche solutions dans knowledge base (17 cas Lexmark C750 intégrés)
5. **Réponse** : Génération réponse personnalisée
6. **Envoi** : Distribution multicanal

## 🚀 Démarrage Rapide

### 1. Prérequis

- **Python 3.8+**
- **MySQL 8.0+** installé et en cours d'exécution
- **Git** (optionnel)

```bash
python3 --version
mysql --version
```

### 2. Installation

```bash
# Cloner le repo (ou télécharger)
git clone https://github.com/hatimhaddou/Hackaton-2025-IA-au-service-des-PME-.git
cd hackathon2025

# Créer environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copier le template de config
cp .env.example .env

# Éditer .env avec vos paramètres MySQL
nano .env  # ou vim/gedit/code
```

Exemple `.env` :
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=votre_mdp_mysql
DB_NAME=printer_support
API_PORT=8000
API_HOST=0.0.0.0
```

### 4. Créer la Base de Données

```bash
# Se connecter à MySQL
mysql -u root -p

# Créer la base
CREATE DATABASE printer_support CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Importer le schéma
mysql -u root -p printer_support < schema_printer_support.sql

# Peupler avec données de référence
python3 init_database.py
```

Résultat attendu :
```
Base de donnees initialisee
Modeles imprimantes : 1
Entrees knowledge base : 17
Clients crees : 3
Appareils crees : 3
```

### 5. Lancer l'API

```bash
# Démarrer FastAPI
python3 api.py

# Ou avec uvicorn directement
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

API accessible sur : **http://localhost:8000**  
Documentation interactive : **http://localhost:8000/docs**

## 📡 Accès Distant (Port Forwarding)

Pour permettre aux collaborateurs d'accéder à la BDD depuis d'autres machines :

### Option 1 : MySQL Direct (port 3306)

```bash
# Éditer /etc/mysql/mysql.conf.d/mysqld.cnf
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Changer bind-address
bind-address = 0.0.0.0  # au lieu de 127.0.0.1

# Redémarrer MySQL
sudo systemctl restart mysql

# Créer utilisateur distant
mysql -u root -p
CREATE USER 'remote_user'@'%' IDENTIFIED BY 'mot_de_passe_fort';
GRANT ALL PRIVILEGES ON printer_support.* TO 'remote_user'@'%';
FLUSH PRIVILEGES;
EXIT;

# Ouvrir port sur firewall
sudo ufw allow 3306/tcp
```

**Connexion depuis machine distante** :
```bash
mysql -h IP_DE_VOTRE_PC -u remote_user -p printer_support
```

### Option 2 : API REST (port 8000 - RECOMMANDÉ)

Plus sécurisé que d'exposer MySQL directement.

```bash
# Ouvrir port API sur firewall
sudo ufw allow 8000/tcp

# Lancer API en mode production
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

**Accès depuis navigateur** :
- Documentation : `http://IP_DE_VOTRE_PC:8000/docs`
- Health check : `http://IP_DE_VOTRE_PC:8000/health`
- Tickets : `http://IP_DE_VOTRE_PC:8000/tickets`

**Exemple requête depuis autre machine (Python)** :
```python
import requests

# Créer un ticket
response = requests.post('http://IP_SERVEUR:8000/tickets', json={
    'customer_id': 1,
    'subject': 'Imprimante bloquée',
    'description': 'Le panneau de commandes n\'affiche rien',
    'priority': 'high'
})
print(response.json())

# Rechercher dans la KB
response = requests.post('http://IP_SERVEUR:8000/knowledge/search', json={
    'query': 'panneau commandes ne s\'affiche pas',
    'model_filter': 'C750',
    'limit': 3
})
print(response.json())
```

### Option 3 : SSH Tunnel (temporaire/dev)

```bash
# Sur machine distante
ssh -L 8000:localhost:8000 user@IP_SERVEUR

# Puis accéder à http://localhost:8000 depuis la machine distante
```

## 📊 Structure de la Base de Données

### Tables Principales

| Table | Description |
|-------|-------------|
| `customers` | Clients (entreprises utilisant les imprimantes) |
| `printer_models` | Catalogue modèles imprimantes supportés |
| `devices` | Appareils déployés chez les clients |
| `knowledge_base` | Base de connaissance (17 problèmes Lexmark C750) |
| `tickets` | Tickets de support |
| `messages` | Messages entrants/sortants (email, SMS, chat, call) |
| `attachments` | Pièces jointes (logs, photos, PDF) |
| `extractions` | Données extraites par IA (modèle, erreur, SN) |
| `rag_results` | Résultats recherche RAG (KB matching) |
| `predictions` | Classifications IA (catégorie ticket) |
| `responses` | Réponses générées par IA |
| `outbound_logs` | Historique envois multicanaux |
| `processing_steps` | Traçabilité étapes pipeline |
| `ticket_history` | Audit modifications tickets |
| `automation_metrics` | KPI performance IA |

### Vues

- `v_actionable_tickets` : Tickets nécessitant action humaine
- `v_pipeline_performance` : Métriques quotidiennes IA
- `v_unprocessed_messages` : Messages en attente traitement

## 🔧 Endpoints API Principaux

### Health & Info
- `GET /` - Info service
- `GET /health` - Health check DB

### Customers
- `GET /customers` - Liste clients
- `POST /customers` - Créer client

### Tickets
- `GET /tickets` - Liste tickets (filtres : status, priority)
- `POST /tickets` - Créer ticket
- `GET /tickets/{id}` - Détails complets (messages, extractions, RAG, réponses)

### Messages
- `POST /messages` - Ingérer message (email/SMS/chat/call)
- `GET /messages/unprocessed` - Messages non traités

### Knowledge Base
- `POST /knowledge/search` - Recherche RAG (requête → solutions KB)

### Extractions
- `POST /extractions` - Enregistrer extraction IA

### Stats
- `GET /stats/pipeline` - Performance pipeline (30 derniers jours)
- `GET /stats/tickets` - Répartition tickets (statut, priorité)

### Models
- `GET /models` - Modèles imprimantes supportés

## 📦 Fichiers du Projet

```
hackathon2025/
├── api.py                          # API REST FastAPI
├── init_database.py                # Script initialisation MySQL
├── schema_printer_support.sql      # Schéma complet MySQL
├── requirements.txt                # Dépendances Python
├── .env.example                    # Template configuration
├── .gitignore                      # Git ignore rules
├── README.md                       # Cette doc
└── data/
    └── reference_data.json         # Données référence (Lexmark C750 + 17 KB)
```

## 🧪 Tests Rapides

```bash
# Test connexion DB
mysql -u root -p printer_support -e "SELECT COUNT(*) FROM knowledge_base;"

# Test API health
curl http://localhost:8000/health

# Lister modèles
curl http://localhost:8000/models

# Recherche KB
curl -X POST http://localhost:8000/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query": "impression floue", "limit": 3}'
```

## 🚧 Prochaines Étapes (TODO)

- [ ] Implémenter module classification IA (catégorisation tickets)
- [ ] Implémenter extracteur NER (modèle imprimante, code erreur)
- [ ] Intégrer embeddings vectoriels pour RAG (au lieu de FULLTEXT)
- [ ] Connecter API envoi email/SMS (Twilio, SendGrid)
- [ ] Ajouter authentification API (JWT tokens)
- [ ] Dashboard temps réel (monitoring pipeline)
- [ ] Tests unitaires (pytest)

## 📄 Licence

Projet hackathon 2025 - IA au service des PME

## 👥 Contact

Repository : [github.com/hatimhaddou/Hackaton-2025-IA-au-service-des-PME-](https://github.com/hatimhaddou/Hackaton-2025-IA-au-service-des-PME-)
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
