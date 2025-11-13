"""
Setup complet SQLite pour le hackathon
Crée la base + insère toutes les données automatiquement
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random

# ============================================
# CONFIGURATION
# ============================================

DB_FILE = 'support_client.db'

# ============================================
# CRÉATION DU SCHÉMA
# ============================================

def create_schema(conn):
    """Crée toutes les tables SQLite"""
    cursor = conn.cursor()
    
    # Table CLIENTS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        client_id TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telephone TEXT,
        entreprise TEXT,
        type_licence TEXT,
        niveau_technique TEXT DEFAULT 'moyen',
        nombre_tickets_total INTEGER DEFAULT 0,
        nombre_tickets_resolus_auto INTEGER DEFAULT 0,
        taux_satisfaction REAL,
        derniere_interaction TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table TICKETS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id TEXT PRIMARY KEY,
        client_id TEXT,
        channel TEXT NOT NULL,
        subject TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        subcategory TEXT,
        priority TEXT,
        status TEXT DEFAULT 'new',
        auto_resolvable INTEGER,
        confidence_score REAL,
        resolution_type TEXT,
        resolution_applied TEXT,
        estimated_resolution_time TEXT,
        actual_resolution_time INTEGER,
        assigned_to TEXT,
        escalated INTEGER DEFAULT 0,
        escalation_reason TEXT,
        client_rating INTEGER,
        client_feedback TEXT,
        knowledge_base_ref TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        resolved_at TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )
    ''')
    
    # Table RESOLUTIONS (Base de connaissance)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resolutions (
        resolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        subcategory TEXT,
        problem_description TEXT NOT NULL,
        solution_title TEXT NOT NULL,
        solution_steps TEXT NOT NULL,
        solution_full_text TEXT,
        success_rate REAL,
        times_used INTEGER DEFAULT 0,
        average_resolution_time INTEGER,
        knowledge_base_ref TEXT UNIQUE NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table TICKET_HISTORY
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticket_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        action TEXT NOT NULL,
        action_by TEXT,
        action_details TEXT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
    )
    ''')
    
    # Index pour performances
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tickets_client ON tickets(client_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category)')
    
    conn.commit()
    print("Schéma de base de données créé")

# ============================================
# INSERTION DES CLIENTS
# ============================================

def insert_clients(conn):
    """Insère 48 clients de test"""
    cursor = conn.cursor()
    
    clients_data = [
        ('CL001', 'Dubois', 'Marie', 'marie.dubois@email.com', '+33612345601', 'Tech Solutions SA', 'Microsoft 365 Business', 'moyen'),
        ('CL002', 'Martin', 'Jean', 'jean.martin@company.fr', '+33612345602', 'Martin SARL', 'Microsoft 365 Famille', 'debutant'),
        ('CL003', 'Bernard', 'Sophie', 'sophie.bernard@corp.com', '+33612345603', 'Corp Industries', 'Microsoft 365 Entreprise', 'avance'),
        ('CL004', 'Petit', 'Luc', 'luc.petit@mail.fr', '+33612345604', None, 'Microsoft 365 Famille', 'moyen'),
        ('CL005', 'Robert', 'Julie', 'julie.robert@startup.io', '+33612345605', 'Startup Innov', 'Microsoft 365 Business', 'avance'),
        ('CL006', 'Richard', 'Pierre', 'pierre.richard@finance.fr', '+33612345606', 'Finance Corp', 'Microsoft 365 Entreprise', 'moyen'),
        ('CL007', 'Durand', 'Isabelle', 'i.durand@perso.fr', '+33612345607', None, 'Personnel', 'debutant'),
        ('CL008', 'Moreau', 'Thomas', 'thomas.moreau@agency.com', '+33612345608', 'Creative Agency', 'Microsoft 365 Business', 'avance'),
        ('CL009', 'Simon', 'Claire', 'claire.simon@mobile.fr', '+33612345609', None, 'Microsoft 365 Famille', 'moyen'),
        ('CL010', 'Laurent', 'Marc', 'marc.laurent@cloud.tech', '+33612345610', 'Cloud Tech', 'Microsoft 365 Business', 'moyen'),
    ]
    
    # Générer 38 clients supplémentaires
    prenoms = ['Anne', 'David', 'Laura', 'Vincent', 'Emma', 'Nicolas', 'Sarah', 'Alexandre', 'Camille', 'Julien',
               'Charlotte', 'Hugo', 'Léa', 'Maxime', 'Alice', 'Lucas', 'Manon', 'Nathan', 'Chloé', 'Tom',
               'Inès', 'Louis', 'Jade', 'Théo', 'Zoé', 'Adam', 'Lola', 'Gabriel', 'Eva', 'Raphael',
               'Lina', 'Arthur', 'Louise', 'Paul', 'Anna', 'Jules', 'Rose', 'Ethan']
    
    noms = ['Lefebvre', 'Roux', 'Fournier', 'Girard', 'Bonnet', 'Lambert', 'Fontaine', 'Rousseau', 'Vincent', 'Muller',
            'Leroy', 'Garnier', 'Chevalier', 'Francois', 'Mercier', 'Blanc', 'Guerin', 'Boyer', 'Faure', 'Andre',
            'Renard', 'Arnaud', 'Barbier', 'Denis', 'Aubry', 'Bertrand', 'Roy', 'Henry', 'Colin', 'Vidal',
            'Perez', 'Lemaire', 'Gauthier', 'Perrin', 'Morel', 'Dupont', 'Leclerc', 'Carpentier']
    
    for i in range(11, 49):
        client_id = f'CL{i:03d}'
        nom = noms[i-11]
        prenom = prenoms[i-11]
        email = f'{prenom.lower()}.{nom.lower()}@example{i}.com'
        tel = f'+3361234{5600+i}'
        entreprise = f'Company {i}' if i % 2 == 0 else None
        licence = random.choice(['Microsoft 365 Famille', 'Microsoft 365 Business', 'Microsoft 365 Entreprise'])
        niveau = random.choice(['debutant', 'moyen', 'avance'])
        clients_data.append((client_id, nom, prenom, email, tel, entreprise, licence, niveau))
    
    # Utiliser INSERT OR IGNORE pour rendre l'opération idempotente
    cursor.executemany('''
        INSERT OR IGNORE INTO clients (client_id, nom, prenom, email, telephone, entreprise, type_licence, niveau_technique)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', clients_data)
    
    conn.commit()
    print(f"{len(clients_data)} clients insérés")

# ============================================
# INSERTION DES RÉSOLUTIONS
# ============================================

def insert_resolutions(conn):
    """Insère la base de connaissance"""
    cursor = conn.cursor()
    
    resolutions = [
        ('authentification', 'outlook_login', 'Impossible de se connecter à Outlook', 
         'Réinitialisation mot de passe Outlook',
         '["Vérifier Caps Lock", "Aller sur account.microsoft.com", "Réinitialiser mot de passe", "Vider cache", "Retenter"]',
         'Réinitialiser le mot de passe via account.microsoft.com', 0.95, 245, 5, 'KB-AUTH-001'),
        
        ('licence', 'office365_activation', 'Licence Office 365 expirée après renouvellement',
         'Rafraîchissement licence Office 365',
         '["Se déconnecter", "Attendre 15 min", "Se reconnecter", "Vérifier statut"]',
         'Attendre la propagation de la licence (15-20 minutes)', 0.92, 187, 20, 'KB-LIC-003'),
        
        ('technique', 'teams_crash', 'Teams plante au démarrage',
         'Réparation Microsoft Teams',
         '["Fermer Teams", "Supprimer cache", "Redémarrer", "Réinstaller si échec"]',
         'Supprimer le cache Teams et redémarrer', 0.89, 312, 10, 'KB-TEAMS-007'),
        
        ('synchronisation', 'onedrive_sync', 'OneDrive ne synchronise plus',
         'Redémarrage synchronisation OneDrive',
         '["Dissocier PC", "Se reconnecter", "Vérifier espace"]',
         'Dissocier puis reconnecter le compte OneDrive', 0.87, 423, 8, 'KB-SYNC-002'),
        
        ('facturation', 'invoice_request', 'Facture introuvable',
         'Téléchargement facture Microsoft',
         '["account.microsoft.com", "Facturation", "Historique", "Télécharger PDF"]',
         'Télécharger depuis account.microsoft.com > Facturation', 0.98, 156, 5, 'KB-BILL-001'),
    ]
    
    # Idempotent insert
    cursor.executemany('''
        INSERT OR IGNORE INTO resolutions (category, subcategory, problem_description, solution_title, 
                                solution_steps, solution_full_text, success_rate, times_used, 
                                average_resolution_time, knowledge_base_ref)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', resolutions)
    
    conn.commit()
    print(f"{len(resolutions)} résolutions insérées")

# ============================================
# INSERTION DES TICKETS (depuis JSON)
# ============================================

def insert_tickets_from_json(conn, json_file='tickets.json'):
    """Insère les tickets depuis le fichier JSON (par défaut `tickets.json`).

    Si le fichier fourni est introuvable, essaie aussi `microsoft_tickets_dataset.json`.
    En dernier recours, crée des tickets de démonstration.
    """
    tickets = None
    tried = []
    for candidate in (json_file, 'microsoft_tickets_dataset.json'):
        try:
            tried.append(candidate)
            with open(candidate, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
                break
        except FileNotFoundError:
            continue

    if tickets is None:
        print(f"Aucun fichier trouvé ({', '.join(tried)}). Création de tickets de démo...")
        tickets = create_demo_tickets()
    
    cursor = conn.cursor()
    
    for ticket in tickets:
        # Calculer confiance et statut
        if ticket.get('auto_resolvable'):
            status = 'auto_resolved'
            confidence = 0.85 + random.random() * 0.14  # 0.85-0.99
            assigned_to = 'IA'
        else:
            status = 'escalated'
            confidence = 0.60 + random.random() * 0.15  # 0.60-0.75
            assigned_to = 'Agent Humain'
        # INSERT OR IGNORE pour éviter les doublons si on relance le setup
        cursor.execute('''
            INSERT OR IGNORE INTO tickets (
                ticket_id, client_id, channel, subject, content,
                category, subcategory, priority, auto_resolvable,
                resolution_type, estimated_resolution_time,
                knowledge_base_ref, status, confidence_score, assigned_to, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticket['ticket_id'],
            ticket['client_id'],
            ticket['channel'],
            ticket['subject'],
            ticket['content'],
            ticket['category'],
            ticket['subcategory'],
            ticket['priority'],
            1 if ticket['auto_resolvable'] else 0,
            ticket['resolution_type'],
            ticket['estimated_resolution_time'],
            ticket['knowledge_base_ref'],
            status,
            round(confidence, 2),
            assigned_to,
            ticket['timestamp']
        ))
    
    conn.commit()
    print(f"{len(tickets)} tickets insérés")
    
    # Mettre à jour les compteurs clients
    update_client_counts(conn)

def create_demo_tickets():
    """Crée 10 tickets de démo si le JSON est absent"""
    base_date = datetime.now() - timedelta(days=7)
    
    tickets = []
    for i in range(1, 11):
        tickets.append({
            'ticket_id': f'TK{i:03d}',
            'client_id': f'CL{i:03d}',
            'channel': random.choice(['email', 'sms', 'phone']),
            'subject': f'Problème de test #{i}',
            'content': f'Contenu du ticket de test numéro {i}',
            'category': random.choice(['authentification', 'licence', 'technique']),
            'subcategory': 'test',
            'priority': random.choice(['low', 'medium', 'high']),
            'auto_resolvable': i % 2 == 0,
            'resolution_type': 'test_resolution',
            'estimated_resolution_time': f'{random.randint(5, 30)}min',
            'knowledge_base_ref': f'KB-TEST-{i:03d}',
            'timestamp': (base_date + timedelta(days=i)).isoformat()
        })
    
    return tickets

def update_client_counts(conn):
    """Met à jour les compteurs de tickets par client"""
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE clients 
        SET nombre_tickets_total = (
            SELECT COUNT(*) FROM tickets WHERE tickets.client_id = clients.client_id
        ),
        nombre_tickets_resolus_auto = (
            SELECT COUNT(*) FROM tickets 
            WHERE tickets.client_id = clients.client_id AND tickets.status = 'auto_resolved'
        ),
        derniere_interaction = (
            SELECT MAX(created_at) FROM tickets WHERE tickets.client_id = clients.client_id
        )
    ''')
    
    conn.commit()
    print("Compteurs clients mis à jour")

# ============================================
# STATISTIQUES
# ============================================

def display_stats(conn):
    """Affiche les statistiques de la base"""
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("STATISTIQUES DE LA BASE DE DONNÉES")
    print("="*60)
    
    # Stats globales
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN auto_resolvable = 1 THEN 1 ELSE 0 END) as auto_resolvable,
            SUM(CASE WHEN status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved,
            AVG(confidence_score) as avg_confidence,
            SUM(CASE WHEN escalated = 1 THEN 1 ELSE 0 END) as escalated
        FROM tickets
    ''')
    
    stats = cursor.fetchone()
    total, auto_resolvable, auto_resolved, avg_conf, escalated = stats
    
    automation_rate = (auto_resolved / total * 100) if total > 0 else 0
    
    print(f"\n Vue d'ensemble:")
    print(f"  • Total tickets: {total}")
    print(f"  • Auto-résolvables: {auto_resolvable} ({auto_resolvable/total*100:.1f}%)")
    print(f"  • Auto-résolus: {auto_resolved}")
    print(f"  • Score confiance moyen: {avg_conf:.2f}")
    print(f"  • Tickets escaladés: {escalated}")
    print(f"  •  Taux d'automatisation: {automation_rate:.1f}%")
    
    # Stats par canal
    cursor.execute('''
        SELECT channel, COUNT(*), 
               SUM(CASE WHEN status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved
        FROM tickets 
        GROUP BY channel
    ''')
    
    print(f"\n Par canal:")
    for row in cursor.fetchall():
        channel, total_ch, auto = row
        print(f"  • {channel}: {total_ch} tickets ({auto} auto-résolus)")
    
    # Top catégories
    cursor.execute('''
        SELECT category, COUNT(*) as count
        FROM tickets
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
        LIMIT 5
    ''')
    
    print(f"\n Top 5 catégories:")
    for i, row in enumerate(cursor.fetchall(), 1):
        category, count = row
        print(f"  {i}. {category}: {count} tickets")
    
    # Clients actifs
    cursor.execute('SELECT COUNT(*) FROM clients WHERE nombre_tickets_total > 0')
    active_clients = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM clients')
    total_clients = cursor.fetchone()[0]
    
    print(f"\n Clients:")
    print(f"  • Total: {total_clients}")
    print(f"  • Actifs: {active_clients}")
    
    print("\n" + "="*60)

# ============================================
# REQUÊTES UTILES
# ============================================

# (Requêtes exemples supprimées — elles n'appartiennent pas au script de création de la base)

# ============================================
# MAIN
# ============================================

def main():
    """Fonction principale - Setup complet"""
    print("\n" + "="*60)
    print(" SETUP SQLITE - SUPPORT CLIENT IA")
    print("="*60 + "\n")
    
    # Connexion
    print(f" Création de la base: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    
    try:
        # Création
        create_schema(conn)
        insert_clients(conn)
        insert_resolutions(conn)
        insert_tickets_from_json(conn)
        
        # Stats
        display_stats(conn)
        
        print(f"\n Setup terminé avec succès!")
        print(f" Base de données créée: {DB_FILE}")
        print(f" Taille: {conn.execute('SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()').fetchone()[0] / 1024:.1f} KB")
        print(f"\n Partage simplement le fichier '{DB_FILE}' avec ton équipe!")
        
    except Exception as e:
        print(f"\n Erreur: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
