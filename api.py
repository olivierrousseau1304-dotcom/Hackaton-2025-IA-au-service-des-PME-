"""
API REST FastAPI pour support imprimantes IA
Endpoints pour interroger la base MySQL et gérer le pipeline
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Printer Support API",
    description="API pour support imprimantes avec pipeline IA (classification → extraction → RAG → réponse)",
    version="1.0.0"
)

# CORS pour permettre accès depuis navigateur/autres machines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: spécifier domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# CONFIGURATION DATABASE
# =====================================================

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'printer_support'),
    'charset': 'utf8mb4'
}

def get_db():
    """Obtenir connexion DB"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erreur DB: {str(e)}")
    finally:
        if conn.is_connected():
            conn.close()

# =====================================================
# MODELS PYDANTIC
# =====================================================

class Customer(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

class TicketCreate(BaseModel):
    customer_id: int
    device_id: Optional[int] = None
    subject: str
    description: str
    priority: Optional[str] = 'medium'

class MessageCreate(BaseModel):
    customer_id: Optional[int] = None
    channel: str  # email, sms, call, chat
    direction: str = 'inbound'  # inbound, outbound
    subject: Optional[str] = None
    body: str
    transcription: Optional[str] = None

class ExtractionCreate(BaseModel):
    ticket_id: int
    extractor_name: str
    extracted_fields: Dict[str, Any]
    confidence: Optional[float] = None

class RAGQuery(BaseModel):
    query: str
    model_filter: Optional[str] = None  # filtrer par modèle
    limit: int = 5

# =====================================================
# ENDPOINTS
# =====================================================

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Printer Support API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check(conn = Depends(get_db)):
    """Vérifier connexion DB"""
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    cursor.close()
    return {"status": "healthy", "database": "connected"}

# =====================================================
# CUSTOMERS
# =====================================================

@app.get("/customers")
def list_customers(limit: int = Query(50, le=200), conn = Depends(get_db)):
    """Lister les clients"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM customers ORDER BY created_at DESC LIMIT {limit}")
    customers = cursor.fetchall()
    cursor.close()
    return {"customers": customers, "count": len(customers)}

@app.post("/customers")
def create_customer(customer: Customer, conn = Depends(get_db)):
    """Créer un client"""
    cursor = conn.cursor()
    query = """
        INSERT INTO customers (company_name, contact_name, contact_email, contact_phone, address)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            customer.company_name,
            customer.contact_name,
            customer.contact_email,
            customer.contact_phone,
            customer.address
        ))
        conn.commit()
        customer_id = cursor.lastrowid
        cursor.close()
        return {"customer_id": customer_id, "status": "created"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# =====================================================
# TICKETS
# =====================================================

@app.get("/tickets")
def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = Query(100, le=500),
    conn = Depends(get_db)
):
    """Lister les tickets avec filtres optionnels"""
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = %s"
        params.append(status)
    if priority:
        query += " AND priority = %s"
        params.append(priority)
    
    query += " ORDER BY created_at DESC LIMIT %s"
    params.append(limit)
    
    cursor.execute(query, params)
    tickets = cursor.fetchall()
    cursor.close()
    return {"tickets": tickets, "count": len(tickets)}

@app.post("/tickets")
def create_ticket(ticket: TicketCreate, conn = Depends(get_db)):
    """Créer un nouveau ticket"""
    cursor = conn.cursor()
    query = """
        INSERT INTO tickets (customer_id, device_id, subject, description, priority, status)
        VALUES (%s, %s, %s, %s, %s, 'new')
    """
    try:
        cursor.execute(query, (
            ticket.customer_id,
            ticket.device_id,
            ticket.subject,
            ticket.description,
            ticket.priority
        ))
        conn.commit()
        ticket_id = cursor.lastrowid
        cursor.close()
        
        # TODO: déclencher pipeline (classification → extraction → RAG → réponse)
        
        return {"ticket_id": ticket_id, "status": "created", "next_step": "classification"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, conn = Depends(get_db)):
    """Obtenir un ticket avec détails complets"""
    cursor = conn.cursor(dictionary=True)
    
    # Ticket principal
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = %s", (ticket_id,))
    ticket = cursor.fetchone()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket non trouvé")
    
    # Messages associés
    cursor.execute("SELECT * FROM messages WHERE ticket_id = %s ORDER BY received_at", (ticket_id,))
    messages = cursor.fetchall()
    
    # Extractions
    cursor.execute("SELECT * FROM extractions WHERE ticket_id = %s", (ticket_id,))
    extractions = cursor.fetchall()
    
    # RAG results
    cursor.execute("SELECT * FROM rag_results WHERE ticket_id = %s ORDER BY created_at DESC LIMIT 1", (ticket_id,))
    rag = cursor.fetchone()
    
    # Réponses
    cursor.execute("SELECT * FROM responses WHERE ticket_id = %s ORDER BY created_at", (ticket_id,))
    responses = cursor.fetchall()
    
    cursor.close()
    
    return {
        "ticket": ticket,
        "messages": messages,
        "extractions": extractions,
        "rag_result": rag,
        "responses": responses
    }

# =====================================================
# MESSAGES
# =====================================================

@app.post("/messages")
def create_message(message: MessageCreate, conn = Depends(get_db)):
    """Ingérer un nouveau message (email/SMS/call/chat)"""
    cursor = conn.cursor()
    query = """
        INSERT INTO messages 
        (customer_id, channel, direction, subject, body, transcription, processed)
        VALUES (%s, %s, %s, %s, %s, %s, FALSE)
    """
    try:
        cursor.execute(query, (
            message.customer_id,
            message.channel,
            message.direction,
            message.subject,
            message.body,
            message.transcription
        ))
        conn.commit()
        message_id = cursor.lastrowid
        cursor.close()
        
        # TODO: déclencher traitement pipeline
        
        return {"message_id": message_id, "status": "received", "next_step": "processing"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/unprocessed")
def get_unprocessed_messages(limit: int = Query(50, le=200), conn = Depends(get_db)):
    """Lister les messages non traités"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM v_unprocessed_messages LIMIT %s
    """, (limit,))
    messages = cursor.fetchall()
    cursor.close()
    return {"messages": messages, "count": len(messages)}

# =====================================================
# KNOWLEDGE BASE (RAG)
# =====================================================

@app.post("/knowledge/search")
def search_knowledge_base(rag_query: RAGQuery, conn = Depends(get_db)):
    """Recherche dans la base de connaissance (RAG simplifiée - FULLTEXT search)"""
    cursor = conn.cursor(dictionary=True)
    
    # Recherche FULLTEXT MySQL (basique, à améliorer avec embeddings)
    query = """
        SELECT 
            kb.kb_id, kb.problem_title, kb.problem_description,
            kb.cause, kb.solution, kb.solution_steps, kb.tags,
            pm.manufacturer, pm.model_name,
            MATCH(problem_title, problem_description, cause, solution) AGAINST(%s IN NATURAL LANGUAGE MODE) as relevance
        FROM knowledge_base kb
        LEFT JOIN printer_models pm ON kb.model_id = pm.model_id
        WHERE MATCH(problem_title, problem_description, cause, solution) AGAINST(%s IN NATURAL LANGUAGE MODE)
    """
    
    params = [rag_query.query, rag_query.query]
    
    if rag_query.model_filter:
        query += " AND pm.model_name LIKE %s"
        params.append(f"%{rag_query.model_filter}%")
    
    query += " ORDER BY relevance DESC LIMIT %s"
    params.append(rag_query.limit)
    
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        
        return {
            "query": rag_query.query,
            "results": results,
            "count": len(results)
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Recherche KB: {str(e)}")

# =====================================================
# EXTRACTIONS
# =====================================================

@app.post("/extractions")
def create_extraction(extraction: ExtractionCreate, conn = Depends(get_db)):
    """Enregistrer une extraction (données structurées extraites d'un message/ticket)"""
    cursor = conn.cursor()
    query = """
        INSERT INTO extractions 
        (ticket_id, extractor_name, extracted_fields, confidence)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            extraction.ticket_id,
            extraction.extractor_name,
            json.dumps(extraction.extracted_fields),
            extraction.confidence
        ))
        conn.commit()
        extraction_id = cursor.lastrowid
        cursor.close()
        return {"extraction_id": extraction_id, "status": "recorded"}
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# =====================================================
# STATISTICS / MONITORING
# =====================================================

@app.get("/stats/pipeline")
def get_pipeline_stats(conn = Depends(get_db)):
    """Statistiques du pipeline IA"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM v_pipeline_performance ORDER BY date DESC LIMIT 30")
    stats = cursor.fetchall()
    cursor.close()
    return {"pipeline_performance": stats}

@app.get("/stats/tickets")
def get_ticket_stats(conn = Depends(get_db)):
    """Statistiques tickets"""
    cursor = conn.cursor(dictionary=True)
    
    # Répartition par statut
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM tickets 
        GROUP BY status
    """)
    by_status = cursor.fetchall()
    
    # Répartition par priorité
    cursor.execute("""
        SELECT priority, COUNT(*) as count 
        FROM tickets 
        GROUP BY priority
    """)
    by_priority = cursor.fetchall()
    
    # Total
    cursor.execute("SELECT COUNT(*) as total FROM tickets")
    total = cursor.fetchone()['total']
    
    cursor.close()
    
    return {
        "total_tickets": total,
        "by_status": by_status,
        "by_priority": by_priority
    }

# =====================================================
# PRINTER MODELS
# =====================================================

@app.get("/models")
def list_printer_models(conn = Depends(get_db)):
    """Lister les modèles d'imprimantes supportés"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM printer_models ORDER BY manufacturer, model_name")
    models = cursor.fetchall()
    cursor.close()
    return {"models": models, "count": len(models)}

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
