"""
Script de chargement des données JSON vers MySQL
Charge les clients, résolutions et tickets depuis tickets.json
"""

import json
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random
import argparse
import sys

def get_db_connection(host, user, password, database):
    """Crée une connexion MySQL"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            use_unicode=True
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion: {e}")
        sys.exit(1)

def insert_clients(conn, num_clients=48):
    """Insère les clients de test"""
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
    
    prenoms = ['Anne', 'David', 'Laura', 'Vincent', 'Emma', 'Nicolas', 'Sarah', 'Alexandre', 'Camille', 'Julien',
               'Charlotte', 'Hugo', 'Léa', 'Maxime', 'Alice', 'Lucas', 'Manon', 'Nathan', 'Chloé', 'Tom',
               'Inès', 'Louis', 'Jade', 'Théo', 'Zoé', 'Adam', 'Lola', 'Gabriel', 'Eva', 'Raphael',
               'Lina', 'Arthur', 'Louise', 'Paul', 'Anna', 'Jules', 'Rose', 'Ethan']
    
    noms = ['Lefebvre', 'Roux', 'Fournier', 'Girard', 'Bonnet', 'Lambert', 'Fontaine', 'Rousseau', 'Vincent', 'Muller',
            'Leroy', 'Garnier', 'Chevalier', 'Francois', 'Mercier', 'Blanc', 'Guerin', 'Boyer', 'Faure', 'Andre',
            'Renard', 'Arnaud', 'Barbier', 'Denis', 'Aubry', 'Bertrand', 'Roy', 'Henry', 'Colin', 'Vidal',
            'Perez', 'Lemaire', 'Gauthier', 'Perrin', 'Morel', 'Dupont', 'Leclerc', 'Carpentier']
    
    for i in range(11, num_clients + 1):
        client_id = f'CL{i:03d}'
        nom = noms[i - 11]
        prenom = prenoms[i - 11]
        email = f'{prenom.lower()}.{nom.lower()}@example{i}.com'
        tel = f'+3361234{5600 + i}'
        entreprise = f'Company {i}' if i % 2 == 0 else None
        licence = random.choice(['Microsoft 365 Famille', 'Microsoft 365 Business', 'Microsoft 365 Entreprise'])
        niveau = random.choice(['debutant', 'moyen', 'avance'])
        clients_data.append((client_id, nom, prenom, email, tel, entreprise, licence, niveau))
    
    insert_query = """
        INSERT IGNORE INTO clients 
        (client_id, nom, prenom, email, telephone, entreprise, type_licence, niveau_technique)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.executemany(insert_query, clients_data)
        conn.commit()
        print(f"[OK] {len(clients_data)} clients insérés/mis à jour")
    except Error as e:
        print(f"[ERREUR] Insertion clients: {e}")
        conn.rollback()
    finally:
        cursor.close()

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
    
    insert_query = """
        INSERT IGNORE INTO resolutions 
        (category, subcategory, problem_description, solution_title, solution_steps, 
         solution_full_text, success_rate, times_used, average_resolution_time, knowledge_base_ref)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.executemany(insert_query, resolutions)
        conn.commit()
        print(f"[OK] {len(resolutions)} résolutions insérées/mises à jour")
    except Error as e:
        print(f"[ERREUR] Insertion résolutions: {e}")
        conn.rollback()
    finally:
        cursor.close()

def insert_tickets_from_json(conn, json_file='tickets.json'):
    """Insère les tickets depuis le fichier JSON"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
    except FileNotFoundError:
        print(f"[ERREUR] Fichier {json_file} introuvable")
        return 0
    
    cursor = conn.cursor()
    
    insert_query = """
        INSERT IGNORE INTO tickets 
        (ticket_id, client_id, channel, subject, content,
         category, subcategory, priority, auto_resolvable,
         resolution_type, estimated_resolution_time,
         knowledge_base_ref, status, confidence_score, assigned_to, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    inserted_count = 0
    try:
        for ticket in tickets:
            if ticket.get('auto_resolvable'):
                status = 'auto_resolved'
                confidence = 0.85 + random.random() * 0.14
                assigned_to = 'IA'
            else:
                status = 'escalated'
                confidence = 0.60 + random.random() * 0.15
                assigned_to = 'Agent Humain'
            
            cursor.execute(insert_query, (
                ticket['ticket_id'],
                ticket['client_id'],
                ticket['channel'],
                ticket['subject'],
                ticket['content'],
                ticket['category'],
                ticket['subcategory'],
                ticket['priority'],
                1 if ticket.get('auto_resolvable') else 0,
                ticket['resolution_type'],
                ticket['estimated_resolution_time'],
                ticket['knowledge_base_ref'],
                status,
                round(confidence, 2),
                assigned_to,
                ticket['timestamp']
            ))
            inserted_count += 1
        
        conn.commit()
        print(f"[OK] {inserted_count} tickets insérés/mis à jour")
        return inserted_count
    except Error as e:
        print(f"[ERREUR] Insertion tickets: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()

def update_client_counts(conn):
    """Met à jour les compteurs de tickets par client"""
    cursor = conn.cursor()
    
    try:
        update_query = """
            UPDATE clients 
            SET 
                nombre_tickets_total = (
                    SELECT COUNT(*) FROM tickets WHERE tickets.client_id = clients.client_id
                ),
                nombre_tickets_resolus_auto = (
                    SELECT COUNT(*) FROM tickets 
                    WHERE tickets.client_id = clients.client_id AND tickets.status = 'auto_resolved'
                ),
                derniere_interaction = (
                    SELECT MAX(created_at) FROM tickets WHERE tickets.client_id = clients.client_id
                )
        """
        cursor.execute(update_query)
        conn.commit()
        print("[OK] Compteurs clients mis à jour")
    except Error as e:
        print(f"[ERREUR] Mise à jour compteurs: {e}")
        conn.rollback()
    finally:
        cursor.close()

def display_stats(conn):
    """Affiche les statistiques de la base"""
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("STATISTIQUES DE LA BASE MYSQL")
    print("=" * 60)
    
    try:
        # Stats globales
        stats_query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN auto_resolvable = 1 THEN 1 ELSE 0 END) as auto_resolvable,
                SUM(CASE WHEN status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved,
                AVG(confidence_score) as avg_confidence,
                SUM(CASE WHEN escalated = 1 THEN 1 ELSE 0 END) as escalated
            FROM tickets
        """
        
        cursor.execute(stats_query)
        stats = cursor.fetchone()
        total, auto_resolvable, auto_resolved, avg_conf, escalated = stats
        
        if total > 0:
            automation_rate = (auto_resolved / total * 100)
        else:
            automation_rate = 0
        
        print(f"\nVue d'ensemble:")
        print(f"  • Total tickets: {total}")
        print(f"  • Auto-résolvables: {auto_resolvable} ({(auto_resolvable/total*100 if total > 0 else 0):.1f}%)")
        print(f"  • Auto-résolus: {auto_resolved}")
        print(f"  • Score confiance moyen: {avg_conf:.2f}")
        print(f"  • Tickets escaladés: {escalated}")
        print(f"  • Taux d'automatisation: {automation_rate:.1f}%")
        
        # Stats par canal
        channel_query = """
            SELECT channel, COUNT(*), 
                   SUM(CASE WHEN status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved
            FROM tickets 
            GROUP BY channel
        """
        cursor.execute(channel_query)
        
        print(f"\nPar canal:")
        for row in cursor.fetchall():
            channel, total_ch, auto = row
            print(f"  • {channel}: {total_ch} tickets ({auto} auto-résolus)")
        
        # Clients actifs
        cursor.execute('SELECT COUNT(*) FROM clients WHERE nombre_tickets_total > 0')
        active_clients = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM clients')
        total_clients = cursor.fetchone()[0]
        
        print(f"\nClients:")
        print(f"  • Total: {total_clients}")
        print(f"  • Actifs: {active_clients}")
        
        print("\n" + "=" * 60)
    
    except Error as e:
        print(f"[ERREUR] Affichage stats: {e}")
    finally:
        cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Charger les données JSON vers MySQL')
    parser.add_argument('--host', default='localhost', help='Hôte MySQL (défaut: localhost)')
    parser.add_argument('--user', default='root', help='Utilisateur MySQL (défaut: root)')
    parser.add_argument('--password', default='', help='Mot de passe MySQL')
    parser.add_argument('--database', required=True, help='Nom de la base de données (obligatoire)')
    parser.add_argument('--json-file', default='tickets.json', help='Chemin du fichier JSON')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("CHARGEMENT DONNEES JSON -> MYSQL")
    print("=" * 60 + "\n")
    
    # Connexion
    print(f"Connexion à MySQL: {args.host}:{args.database}...")
    conn = get_db_connection(args.host, args.user, args.password, args.database)
    print("[OK] Connecté\n")
    
    try:
        # Insertion des données
        insert_clients(conn)
        insert_resolutions(conn)
        insert_tickets_from_json(conn, args.json_file)
        
        # Mise à jour compteurs
        update_client_counts(conn)
        
        # Stats
        display_stats(conn)
        
        print(f"\n[SUCCES] Chargement des données terminé!")
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        sys.exit(1)
    finally:
        if conn.is_connected():
            conn.close()
            print("\nConnexion fermée.")

if __name__ == "__main__":
    main()
