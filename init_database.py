"""
Script d'initialisation de la base de données MySQL pour support imprimantes IA
Charge les modèles d'imprimantes et la base de connaissance
"""

import mysql.connector
from mysql.connector import Error
import json
import sys
import argparse
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection(host, user, password, database):
    """Créer connexion MySQL"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            use_unicode=True
        )
        print(f"[OK] Connecté à MySQL: {host}/{database}")
        return conn
    except Error as e:
        print(f"[ERREUR] Connexion MySQL: {e}")
        sys.exit(1)

def load_reference_data():
    """Charger les données de référence depuis JSON"""
    data_file = Path(__file__).parent / 'data' / 'reference_data.json'
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERREUR] Fichier {data_file} introuvable")
        sys.exit(1)

def insert_printer_models(conn, models):
    """Insérer les modèles d'imprimantes"""
    cursor = conn.cursor()
    query = """
        INSERT INTO printer_models 
        (manufacturer, model_name, model_code, specifications, manual_url)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            model_code = VALUES(model_code),
            specifications = VALUES(specifications),
            manual_url = VALUES(manual_url)
    """
    
    inserted = 0
    try:
        for model in models:
            cursor.execute(query, (
                model['manufacturer'],
                model['model_name'],
                model.get('model_code'),
                json.dumps(model.get('specifications', {})),
                model.get('manual_url')
            ))
            inserted += 1
        conn.commit()
        print(f"[OK] {inserted} modèles d'imprimantes insérés/mis à jour")
        return cursor.lastrowid
    except Error as e:
        print(f"[ERREUR] Insertion modèles: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def insert_knowledge_base(conn, kb_entries):
    """Insérer la base de connaissance"""
    cursor = conn.cursor()
    
    # Récupérer model_id pour Lexmark C750
    cursor.execute("SELECT model_id FROM printer_models WHERE manufacturer = 'Lexmark' AND model_name = 'C750'")
    result = cursor.fetchone()
    model_id = result[0] if result else None
    
    if not model_id:
        print("[AVERTISSEMENT] Modèle Lexmark C750 non trouvé, KB sera insérée sans model_id")
    
    query = """
        INSERT INTO knowledge_base 
        (model_id, problem_title, problem_description, cause, solution, solution_steps, error_codes, tags, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    inserted = 0
    try:
        for entry in kb_entries:
            cursor.execute(query, (
                model_id,
                entry['problem_title'],
                entry.get('problem_description'),
                entry.get('cause'),
                entry['solution'],
                json.dumps(entry.get('solution_steps', [])),
                json.dumps(entry.get('error_codes', [])),
                json.dumps(entry.get('tags', [])),
                entry.get('source')
            ))
            inserted += 1
        conn.commit()
        print(f"[OK] {inserted} entrées de base de connaissance insérées")
    except Error as e:
        print(f"[ERREUR] Insertion KB: {e}")
        conn.rollback()
    finally:
        cursor.close()

def create_sample_customers(conn):
    """Créer quelques clients d'exemple"""
    cursor = conn.cursor()
    
    customers = [
        ("TechPrint Services", "Jean Dupont", "j.dupont@techprint.fr", "+33612345678", "15 rue de la Tech, 75001 Paris"),
        ("Imprimex SA", "Marie Martin", "m.martin@imprimex.fr", "+33687654321", "23 av des Imprimantes, 69002 Lyon"),
        ("Bureau Solutions", "Pierre Bernard", "p.bernard@bureau-solutions.fr", "+33698765432", "8 bd du Commerce, 33000 Bordeaux"),
    ]
    
    query = """
        INSERT INTO customers 
        (company_name, contact_name, contact_email, contact_phone, address)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        cursor.executemany(query, customers)
        conn.commit()
        print(f"[OK] {len(customers)} clients d'exemple insérés")
    except Error as e:
        print(f"[ERREUR] Insertion clients: {e}")
        conn.rollback()
    finally:
        cursor.close()

def create_sample_devices(conn):
    """Créer quelques imprimantes d'exemple"""
    cursor = conn.cursor()
    
    # Récupérer les IDs
    cursor.execute("SELECT customer_id FROM customers ORDER BY customer_id LIMIT 3")
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT model_id FROM printer_models WHERE model_name = 'C750' LIMIT 1")
    result = cursor.fetchone()
    model_id = result[0] if result else None
    
    if not model_id or not customer_ids:
        print("[AVERTISSEMENT] Pas de modèle ou clients, skip devices")
        cursor.close()
        return
    
    devices = [
        (customer_ids[0], model_id, "LEX-C750-001", "2024-01-15", "2026-01-15", "Bureau principal"),
        (customer_ids[1], model_id, "LEX-C750-002", "2024-03-20", "2026-03-20", "Étage 2"),
        (customer_ids[2], model_id, "LEX-C750-003", "2024-06-10", "2026-06-10", "Salle de réunion"),
    ]
    
    query = """
        INSERT INTO devices 
        (customer_id, model_id, serial_number, install_date, warranty_until, location)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    try:
        cursor.executemany(query, devices)
        conn.commit()
        print(f"[OK] {len(devices)} imprimantes d'exemple insérées")
    except Error as e:
        print(f"[ERREUR] Insertion devices: {e}")
        conn.rollback()
    finally:
        cursor.close()

def display_stats(conn):
    """Afficher les statistiques de la base"""
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("STATISTIQUES BASE DE DONNÉES")
    print("="*60)
    
    tables = [
        ('customers', 'Clients'),
        ('printer_models', 'Modèles imprimantes'),
        ('devices', 'Imprimantes installées'),
        ('knowledge_base', 'Entrées base de connaissance'),
        ('tickets', 'Tickets'),
        ('messages', 'Messages')
    ]
    
    for table, label in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  • {label}: {count}")
        except Error:
            print(f"  • {label}: N/A")
    
    print("="*60 + "\n")
    cursor.close()

def main():
    parser = argparse.ArgumentParser(description='Initialiser la base MySQL pour support imprimantes')
    parser.add_argument('--host', default=os.getenv('DB_HOST', 'localhost'), help='Hôte MySQL')
    parser.add_argument('--user', default=os.getenv('DB_USER', 'root'), help='Utilisateur MySQL')
    parser.add_argument('--password', default=os.getenv('DB_PASSWORD', ''), help='Mot de passe MySQL')
    parser.add_argument('--database', default=os.getenv('DB_NAME', 'printer_support'), help='Nom de la base de données')
    parser.add_argument('--skip-samples', action='store_true', help='Ne pas créer les données d\'exemple')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("INITIALISATION BASE DONNÉES - SUPPORT IMPRIMANTES IA")
    print("="*60 + "\n")
    
    # Connexion
    conn = get_connection(args.host, args.user, args.password, args.database)
    
    try:
        # Charger données de référence
        print("\n[1/5] Chargement données de référence...")
        ref_data = load_reference_data()
        
        # Insérer modèles
        print("[2/5] Insertion modèles d'imprimantes...")
        insert_printer_models(conn, ref_data['printer_models'])
        
        # Insérer KB
        print("[3/5] Insertion base de connaissance...")
        insert_knowledge_base(conn, ref_data['knowledge_base'])
        
        if not args.skip_samples:
            # Créer données d'exemple
            print("[4/5] Création clients d'exemple...")
            create_sample_customers(conn)
            
            print("[5/5] Création imprimantes d'exemple...")
            create_sample_devices(conn)
        else:
            print("[4-5/5] Skip données d'exemple (--skip-samples)")
        
        # Stats
        display_stats(conn)
        
        print("[SUCCÈS] Initialisation terminée!\n")
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        sys.exit(1)
    finally:
        if conn.is_connected():
            conn.close()
            print("Connexion fermée.")

if __name__ == "__main__":
    main()
