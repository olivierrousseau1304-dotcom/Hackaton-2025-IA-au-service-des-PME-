"""
Script pour tester que la base fonctionne
"""

import sqlite3

DB_NAME = 'support_client.db'

def test_database():
    """Test la connexion et affiche quelques données"""
    
    print(" Test de la base de données...\n")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Afficher les 3 premiers tickets
    cursor.execute('SELECT ticket_id, subject, status, confidence_score FROM tickets LIMIT 3')
    tickets = cursor.fetchall()
    
    print("Les 3 premiers tickets :")
    for ticket in tickets:
        print(f"  • {ticket[0]} : {ticket[1]}")
        print(f"    Status: {ticket[2]} | Confiance: {ticket[3]}")
    
    # Stats globales
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved,
            AVG(confidence_score) as avg_confidence
        FROM tickets
    ''')
    
    stats = cursor.fetchone()
    
    print(f"\n Stats :")
    print(f"  • Total : {stats[0]} tickets")
    print(f"  • Auto-résolus : {stats[1]}")
    print(f"  • Taux automatisation : {stats[1]/stats[0]*100:.1f}%")
    print(f"  • Confiance moyenne : {stats[2]:.2f}")
    
    conn.close()
    
    print("\n Base de données fonctionne correctement !")

if __name__ == "__main__":
    test_database()
