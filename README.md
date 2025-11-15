

# 🟦 **HACKAPRINT – ARCHITECTURE GLOBALE & DOCUMENT DE RECONSTRUCTION COMPLÈTE**

### **Version 1.0 — Projet Hackathon IA / Azure AI Foundry / CallRounded / MySQL / APIs Python / SMS & Mails**

---

# 0. INTRODUCTION

HackaPrint est une PME fictive spécialisée dans les services d’impression sur la Côte d’Azur, développée dans un cadre académique et dans la perspective d’un **hackathon IA**.
Le système repose sur :

* un **agent IA téléphonique** (CallRounded)
* des **agents spécialisés Azure AI Foundry**
* une **base MySQL centralisée** (Azure MySQL Flexible Server)
* des **APIs Python (Azure Functions)** qui connectent la voix → IA → BDD
* un **backend modulaire** pour SMS, mails, gestion de tickets
* une **base de connaissance technique**
* un **pipeline de support IT simple** (ITSM léger)
* des **stratégies de sauvegarde & CI/CD GitHub**

Ce document te permet de **tout reconstruire à l’identique**, même si tout ton Azure AI est supprimé.

---

# 1. IDENTITÉ DE L’ENTREPRISE FICTIVE

**Nom : HackaPrint**
**Secteur : Solutions d’impression et maintenance d’imprimantes professionnelles**
**Localisation : Nice, Cannes, Antibes**
**Création : 2018**
**Taille : 23 employés**
**Équipe technique : 6 techniciens support, 1 resp. infrastructure**
**Spécialités :**

* installation & maintenance d’imprimantes
* gestion des consommables
* contrats de location
* dépannage à distance par hotline / IA

Le choix a été influencé par le sujet du hackathon :
👉 **Créer un support IT automatisé multi-canal (voix / SMS / mail) basé sur Azure AI.**

---

# 2. ARCHITECTURE TECHNIQUE GLOBALE

```
                ┌──────────────────────┐
                │      Client           │
                │  (Appel, SMS, Mail)   │
                └─────────┬────────────┘
                          │
                          ▼
               ┌──────────────────────┐
               │     CallRounded      │
               │  (Agent Téléphonique)│
               └─────────┬────────────┘
                          │ Webhooks HTTP
                          ▼
              ┌──────────────────────────┐
              │ Azure Function App (API) │
              │  - get_caller_info       │
              │  - get_order_info        │
              │  - create_ticket         │
              │  - append_message        │
              │  - health_check          │
              └─────────┬───────────────┘
                        │
                        ▼
            ┌─────────────────────────────┐
            │   Azure MySQL Flexible      │
            │   - customers               │
            │   - devices                 │
            │   - tickets                 │
            │   - kb (problèmes → solutions)
            └─────────────────────────────┘

                        ▲
                        │ API Calls depuis Azure AI
                        ▼

             ┌──────────────────────────────┐
             │      Azure AI Foundry        │
             │ - Agent Global               │
             │ - Agent Renseignements       │
             │ - Agent TraitementProblèmes  │
             │ - (option) Agent Email/SMS   │
             │ (prompts versionnés GitHub)  │
             └──────────────────────────────┘

```

---

# 3. STRUCTURE DU REPO GITHUB

```
hackaprint/
│
├── README.md
├── docs/
│   ├── ARCHITECTURE_COMPLETE_HACKAPRINT.md   (ce fichier)
│   ├── AI_AGENTS_OVERVIEW.md
│   ├── FLOW_CALLROUNDED.md
│   ├── EMAIL_SMS_INTEGRATION.md
│   ├── HACKATHON_STRATEGY.md
│   └── BACKUP_STRATEGY.md
│
├── backend/
│   └── function_app/
│       ├── host.json
│       ├── requirements.txt
│       ├── get_caller_info/
│       │   └── __init__.py
│       ├── get_order_info/
│       │   └── __init__.py
│       ├── create_ticket/
│       │   └── __init__.py
│       ├── append_message/
│       │   └── __init__.py
│       └── health_check/
│           └── __init__.py
│
├── database/
│   ├── mysql_schema.sql
│   └── sample_data.sql
│
├── prompts/
│   ├── global_prompt.md
│   ├── renseignements_generaux.md
│   ├── traitement_problemes.md
│   └── ticket_escalation.md
│
└── tools/
    ├── test_api.http
    └── export_guidelines.md

```

---

# 4. BASE DE DONNÉES (MYSQL)

## 4.1. Schéma complet (mysql_schema.sql)

```sql
-- (Déjà fourni précédemment. Remettre ici intégralement.)
```

(tu colles ici exactement la version précédente que je t’ai donnée)

## 4.2. Données d’exemple (sample_data.sql)

```sql
INSERT INTO customers (external_id, name, email, phone, company_name)
VALUES 
('0611223344', 'Jean Martin', 'jean.martin@example.com', '0611223344', 'AzurCompta'),
('0622334455', 'Marie Dupont', 'marie.dupont@example.com', '0622334455', 'CannesPrint');
...
```

---

# 5. BACKEND PYTHON (AZURE FUNCTIONS)

Chaque dossier contient un endpoint relié à CallRounded ou Azure AI Foundry.

Exemple : **get_caller_info**

```python
# code complet déjà fourni plus haut, à remettre dans le repo
```

---

# 6. INTÉGRATION CALLROUNDED (TÉLÉPHONE)

## 6.1. Fonctionnement général

1. Le client appelle HackaPrint.
2. CallRounded interroge ton API pour identifier le client.
3. Variables remplies dans CallRounded :

   * `caller_found_api`
   * `caller_name_api`
   * `caller_company_api`
   * `caller_customer_id`
4. L’agent IA adapté est choisi selon le contexte :

   * Renseignements généraux
   * Problèmes techniques
   * Création de ticket
5. L’IA utilise tes API pour :

   * récupérer des infos sur les appareils
   * créer ou mettre à jour un ticket
   * trouver une solution dans la base de connaissances

## 6.2. Exemple de webhook CallRounded

```
GET https://fa-hackaprint-api.azurewebsites.net/api/get_caller_info?phone={{caller.number}}
```

## 6.3. Prompt de test pour agent “Health Check”

```
Votre seul objectif est de vérifier si le serveur externe répond.
Posez une seule question au technicien :
« Souhaitez-vous que je teste la connexion au serveur ? »
Si oui → appelez l’API health_check.
Répondez ensuite simplement « Connexion OK » ou « Connexion impossible ».
```

---

# 7. AGENTS IA — PROMPTS COMPLETS

## 7.1. Global (global_prompt.md)

(Version fournie dans le message précédent)

## 7.2. Renseignements généraux (renseignements_generaux.md)

## 7.3. Traitement des problèmes (traitement_problemes.md)

## 7.4. Escalade ticket (ticket_escalation.md)

---

# 8. INTÉGRATION EMAIL & SMS

Ton système doit aussi gérer :

* mails entrants → créent des tickets
* réponses mails → attachées au ticket
* SMS entrants → pareil

## 8.1. Architecture simplifiée

```
Email (Outlook / Gmail / n’importe) 
   ↓ via webhook / poller Logic App
Azure Function create_ticket_from_email
   ↓
MySQL → tickets + inbound_messages
```

## 8.2. Pourquoi Gmail échouait ?

Parce que **Google interdit HTTP non sécurisé** pour Gmail connector.
Solution : passer **via l’app 1** (Microsoft), ou utiliser un relais SMTP Gmail hors Logic Apps.

(Comme on en a parlé.)

---

# 9. STRATÉGIE HACKATHON — COMMENT PRÉSENTER TON PROJET

## 9.1. Speech d’ouverture (CEO)

> *"Bienvenue dans un monde où l’IA ne remplace pas l’humain, mais nous libère de tout ce qui nous ralentit. Nous avons imaginé HackaPrint comme un rêve éveillé : un support informatique instantané, naturel, multi-canal, capable de comprendre un appel, un mail ou un SMS, et d’agir en quelques secondes. Ce projet n’est pas seulement une démonstration technique : c’est une nouvelle manière de voir le support client."*

## 9.2. Vision

* IA omnicanale
* Support IT simplifié
* API centralisée
* Solution duplicable à n’importe quelle PME

---

# 10. STRATÉGIE DE BACKUP (BACKUP_STRATEGY.md)

Liste complète déjà fournie plus haut :

* Tout dans GitHub
* Export MySQL régulier
* Export des prompts IA
* Scripts de déploiement ARM/Bicep (optionnel)

---

# 11. COMMENT RECRÉER LE PROJET DE A → Z

## 11.1. 10 étapes exactes

1. Créer le Resource Group
2. Créer Storage Account
3. Créer MySQL Flexible Server
4. Importer mysql_schema.sql
5. Créer Key Vault et stocker secrets
6. Créer Function App Python
7. Déployer les APIs
8. Créer Azure AI Hub
9. Créer Azure AI Project
10. Recréer les agents (copier/coller prompts GitHub)
11. Connecter CallRounded aux endpoints HTTP
12. Tester un appel → doit ouvrir un ticket

---

# 12. VERSION TL;DR (README)

Inclure ceci dans le README du repo :

```
Ce repo contient :
- la base MySQL entièrement reconstituable
- le backend API Python pour CallRounded et Azure AI
- tous les prompts IA
- les docs du projet
- la stratégie de backup
- les explications pour reconstruire l’environnement Azure


