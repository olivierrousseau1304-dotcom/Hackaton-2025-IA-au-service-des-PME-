#!/bin/bash
# Script de test de l'API

API_URL="http://localhost:8000"

echo "======================================"
echo "TESTS API SUPPORT IMPRIMANTES"
echo "======================================"
echo ""

# Test 1: Root
echo "[1] Test endpoint root..."
curl -s $API_URL/ | python3 -m json.tool
echo ""

# Test 2: Health
echo "[2] Test health check..."
curl -s $API_URL/health | python3 -m json.tool
echo ""

# Test 3: Modèles
echo "[3] Liste modèles imprimantes..."
curl -s $API_URL/models | python3 -m json.tool
echo ""

# Test 4: Clients
echo "[4] Liste clients..."
curl -s $API_URL/customers | python3 -m json.tool
echo ""

# Test 5: Tickets
echo "[5] Liste tickets..."
curl -s $API_URL/tickets | python3 -m json.tool
echo ""

# Test 6: Recherche KB
echo "[6] Recherche knowledge base (panneau commandes)..."
curl -s -X POST $API_URL/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query": "panneau commandes ne s'\''affiche rien", "limit": 3}' | python3 -m json.tool
echo ""

# Test 7: Créer ticket
echo "[7] Créer un nouveau ticket..."
curl -s -X POST $API_URL/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "subject": "Imprimante bloquée - erreur bourrage",
    "description": "L'\''imprimante affiche une erreur de bourrage papier mais il n'\''y a pas de papier coincé",
    "priority": "high"
  }' | python3 -m json.tool
echo ""

# Test 8: Stats tickets
echo "[8] Statistiques tickets..."
curl -s $API_URL/stats/tickets | python3 -m json.tool
echo ""

echo "======================================"
echo "TESTS TERMINÉS"
echo "======================================"
