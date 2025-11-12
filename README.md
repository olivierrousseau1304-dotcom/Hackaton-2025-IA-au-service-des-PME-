README 
> **POC — Hackathon CodeForSud x Microsoft @ IMREDD**

## 1) 🎯 Contexte

Les PME font face à une augmentation considérable de demandes clients quotidiennes, sur plusieurs canaux :
📩 Email — 💬 SMS — 📞 Téléphone

Ce traitement manuel mobilise des équipes qualifiées sur des demandes simples et récurrentes, génère des délais et dégrade l'expérience client.

**Constat (cas type) :** 

* **300+ tickets / jour**
* **8 minutes par ticket**
* Jusqu’à **60% automatisables**

=> Environ **1 à 3 ETP mobilisés** à faible valeur ajoutée

> 💡 **Opportunité :**
> Automatiser le traitement des tickets simples pour :
> ✅ Accélérer les délais
> ✅ Réduire les coûts
> ✅ Améliorer la satisfaction client
> ✅ Libérer des agents humains pour les cas complexes

---

## 2) ❗ Problématique

> 🔥 **Comment automatiser intelligemment le traitement des demandes simples afin d’améliorer l’efficacité tout en garantissant des réponses fiables et contextualisées ?**

---

## 3) 🌐 Vision

> « Vers un service Tiers 1 augmenté par l’IA »

Une orchestration intelligente qui :

* Capture les messages multi-canal
* Analyse automatiquement contenu & intention
* Priorise
* Génère des réponses adaptées
* Escalade les cas complexes

---

## 4) ✅ Objectif du POC

> **Démontrer en 3 jours la faisabilité d’un assistant IA capable de traiter automatiquement les demandes simples et d’escalader les complexes.**

Focus MVP :

1. Message entrant (mock)
2. Analyse IA → résumé + catégorie + priorité
3. Décision → auto-réponse / escalade
4. Réponse générée
5. Historisation → dashboard

---

## 5) 🔎 Approche POC vs Produit final

| Fonction             | **POC (3 jours)** | Produit futur           |
| -------------------- | ----------------- | ----------------------- |
| Ingestion multicanal | Mock JSON         | Email / SMS / Téléphone |
| Classification IA    | ✅                 | ✅ Fine-tuning           |
| Vectorisation        | Mini FAQ          | Full historique tickets |
| Orchestration        | Simple            | + ITSM + logistique     |
| Réponse              | Génération simple | Personnalisation        |
| Dashboard            | Basique           | + Analytics avancées    |
| SLA                  | ❌                 | ✅                       |

⚠️ Dans ce hackathon → **POC ciblé**, pas produit industriel.

---

## 6) 🧱 Architecture — MVP

```
   [Entrée message]
         │
         ▼
   Ingestion (mock)
         │
         ▼
 [Azure OpenAI LLM]
  - Analyse
  - Résumé
  - Catégorie
  - Priorité
  - Décision
  - Réponse
         │
   ┌─────┴──────────┐
   ▼                ▼
 Réponse auto     Escalade
                     │
                     ▼
                   DB ticket
         │
         ▼
     Dashboard Web
```

---

## 7) 🤖 Pipeline Agents

| Agent           | Rôle                           |
| --------------- | ------------------------------ |
| Ingestion Agent | Reçoit le message → uniformise |
| LLM Agent       | Analyse + résume + classifie   |
| Routing Agent   | Décide action                  |
| Output Agent    | Gère réponse / ticket          |
| Dashboard Agent | Affiche traitement             |

---

## 8) 🧰 Outils

| Besoin        | Outil                    |
| ------------- | ------------------------ |
| Modèle IA     | Azure OpenAI             |
| Orchestration | Azure Logic Apps         |
| Backend API   | Azure Functions / Python |
| Front         | React / Next.js          |
| DB mock       | JSON / SQLite            |
| Versioning    | GitHub                   |
| Pitch         | PowerPoint / Figma       |

→ Tous gratuits ou avec crédits

---

## 9) 📁 Structure projet

```
/backend
  app.py
  services/
  prompts/

 /frontend
   /pages
   /components

 /data
   tickets.json
   samples.json

 /docs
   architecture.png
   pitch.md

 README.md
```

---

## 10) 👥 Équipe (5)

| Rôle           | Mission             |
| -------------- | ------------------- |
| Backend        | API + logique       |
| IA / Prompting | Analyse + décision  |
| Frontend       | Dashboard           |
| Intégration    | Azure Logic Apps    |
| Pitch / UX     | Storytelling + démo |

---

## 11) 📅 Planning — 3 jours

### ✅ J1 — Analyse + IA

* Comprendre POC
* Créer prompts
* LLM → JSON
* Mock messages
* Sketch UI

> 🎯 LIVRABLE :
> Message → JSON enrichi

---

### ✅ J2 — Produit

* Backend API
* Dashboard
* Routing auto / escalade
* DB tickets

> 🎯 LIVRABLE :
> Message → réponse / ticket

---

### ✅ J3 — Polish + Pitch

* UI clean
* KPI
* Pitch
* Démo fluide

> 🎯 LIVRABLE :
> Démo complète + slides

---

## 12) 🎛️ KPI

* % auto-traités
* Temps moyen
* % escalade
* Satisfaction simulée

---

## 13) 💼 Business value

➡ **60% d’automatisation**
➡ **1,5–3 ETP gagnés**
➡ **ROI < 3 mois**

---

## 14) 🚀 Next steps (post-hackathon)

* Intégration ITSM
* Vectorisation historique
* Recherche sémantique avancée
* Transcription vocale temps réel

