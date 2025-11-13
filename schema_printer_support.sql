-- =====================================================
-- SCHEMA MYSQL - SUPPORT IMPRIMANTES IA
-- Pipeline: Ingestion → Classification → Extraction → RAG → Réponse → Envoi multicanal
-- Compatible MySQL 8.0+
-- =====================================================
-- Importer: mysql -u root -p printer_support < schema_printer_support.sql
-- =====================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

-- =====================================================
-- TABLE: CUSTOMERS (clients PME acheteurs d'imprimantes)
-- =====================================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    address TEXT,
    metadata JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_company (company_name),
    INDEX idx_email (contact_email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Clients PME';

-- =====================================================
-- TABLE: PRINTER_MODELS (modèles d'imprimantes supportés)
-- =====================================================
CREATE TABLE IF NOT EXISTS printer_models (
    model_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    manufacturer VARCHAR(100) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_code VARCHAR(100),
    specifications JSON,
    manual_url VARCHAR(512),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_model (manufacturer, model_name),
    INDEX idx_manufacturer (manufacturer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Modèles imprimantes (Lexmark C750, etc.)';

-- =====================================================
-- TABLE: DEVICES (imprimantes installées chez clients)
-- =====================================================
CREATE TABLE IF NOT EXISTS devices (
    device_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    model_id BIGINT NOT NULL,
    serial_number VARCHAR(255),
    install_date DATE,
    warranty_until DATE,
    location VARCHAR(255),
    metadata JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_model (model_id),
    INDEX idx_serial (serial_number),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (model_id) REFERENCES printer_models(model_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Imprimantes installées';

-- =====================================================
-- TABLE: KNOWLEDGE_BASE (problèmes/causes/solutions référence)
-- =====================================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    kb_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    model_id BIGINT DEFAULT NULL,
    problem_title VARCHAR(512) NOT NULL,
    problem_description TEXT,
    cause VARCHAR(512),
    solution TEXT NOT NULL,
    solution_steps JSON,
    error_codes JSON,
    tags JSON,
    source VARCHAR(255),
    embedding BLOB,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_model (model_id),
    FULLTEXT INDEX ft_problem (problem_title, problem_description, cause, solution),
    FOREIGN KEY (model_id) REFERENCES printer_models(model_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Base de connaissance problèmes/solutions';

-- =====================================================
-- TABLE: TICKETS (un ticket par demande client)
-- =====================================================
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    external_ref VARCHAR(255) UNIQUE,
    customer_id BIGINT NOT NULL,
    device_id BIGINT DEFAULT NULL,
    subject VARCHAR(512),
    description TEXT,
    priority ENUM('low','medium','high','critical') DEFAULT 'medium',
    status ENUM('new','open','in_progress','auto_resolved','escalated','answered','archived','closed') DEFAULT 'new',
    classification_label VARCHAR(255),
    classification_confidence FLOAT,
    assigned_to VARCHAR(255),
    last_activity_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    INDEX idx_customer (customer_id),
    INDEX idx_device (device_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_classification (classification_label),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Tickets support';

-- =====================================================
-- TABLE: MESSAGES (messages entrants/sortants multicanal)
-- =====================================================
CREATE TABLE IF NOT EXISTS messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT DEFAULT NULL,
    customer_id BIGINT DEFAULT NULL,
    channel ENUM('email','sms','call','chat','webhook') NOT NULL,
    direction ENUM('inbound','outbound') NOT NULL,
    external_id VARCHAR(255),
    subject VARCHAR(512),
    body TEXT,
    transcription TEXT,
    raw_payload JSON,
    received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processor_notes JSON,
    INDEX idx_ticket (ticket_id),
    INDEX idx_customer (customer_id),
    INDEX idx_channel (channel),
    INDEX idx_processed (processed),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE SET NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Messages multicanal';

-- =====================================================
-- TABLE: ATTACHMENTS (fichiers joints)
-- =====================================================
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message_id BIGINT NOT NULL,
    filename VARCHAR(512),
    content_type VARCHAR(255),
    size_bytes BIGINT DEFAULT 0,
    storage_ref VARCHAR(1024),
    metadata JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_message (message_id),
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Pièces jointes';

-- =====================================================
-- TABLE: EXTRACTIONS (données extraites par modèles IA)
-- =====================================================
CREATE TABLE IF NOT EXISTS extractions (
    extraction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT DEFAULT NULL,
    message_id BIGINT DEFAULT NULL,
    extractor_name VARCHAR(255) NOT NULL,
    extractor_version VARCHAR(100),
    extracted_fields JSON NOT NULL,
    confidence FLOAT,
    provenance JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    INDEX idx_message (message_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Données extraites (modèle, code erreur, etc.)';

-- =====================================================
-- TABLE: RAG_RESULTS (résultats recherche RAG)
-- =====================================================
CREATE TABLE IF NOT EXISTS rag_results (
    rag_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    query TEXT NOT NULL,
    retrieved_documents JSON NOT NULL,
    combined_score FLOAT,
    retriever VARCHAR(255),
    retriever_version VARCHAR(100),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Résultats RAG';

-- =====================================================
-- TABLE: PREDICTIONS (classifications IA)
-- =====================================================
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT DEFAULT NULL,
    message_id BIGINT DEFAULT NULL,
    model_name VARCHAR(255) NOT NULL,
    model_version VARCHAR(100),
    task ENUM('classification','priority_estimation','intent_detection') DEFAULT 'classification',
    label VARCHAR(255),
    confidence FLOAT,
    meta JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    INDEX idx_message (message_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Prédictions IA';

-- =====================================================
-- TABLE: RESPONSES (réponses générées)
-- =====================================================
CREATE TABLE IF NOT EXISTS responses (
    response_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    rag_id BIGINT DEFAULT NULL,
    responder_type ENUM('auto','agent') NOT NULL,
    responder_id VARCHAR(255),
    channel ENUM('email','sms','call','chat') NOT NULL,
    content TEXT NOT NULL,
    content_json JSON,
    send_payload JSON,
    sent_at DATETIME,
    send_status ENUM('queued','sent','delivered','failed','ignored') DEFAULT 'queued',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    INDEX idx_status (send_status),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (rag_id) REFERENCES rag_results(rag_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Réponses générées';

-- =====================================================
-- TABLE: OUTBOUND_LOGS (logs envois multicanal)
-- =====================================================
CREATE TABLE IF NOT EXISTS outbound_logs (
    outbound_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    response_id BIGINT DEFAULT NULL,
    channel ENUM('email','sms','call','chat') NOT NULL,
    provider VARCHAR(255),
    provider_response_code VARCHAR(255),
    provider_response JSON,
    attempted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT FALSE,
    INDEX idx_response (response_id),
    FOREIGN KEY (response_id) REFERENCES responses(response_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Logs envois';

-- =====================================================
-- TABLE: PROCESSING_STEPS (suivi pipeline par ticket)
-- =====================================================
CREATE TABLE IF NOT EXISTS processing_steps (
    step_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    step_name ENUM('ingestion','classification','extraction','rag','response_generation','send','postprocess') NOT NULL,
    status ENUM('pending','in_progress','success','failed') NOT NULL DEFAULT 'pending',
    started_at DATETIME,
    finished_at DATETIME,
    details JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    INDEX idx_step (step_name),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Étapes pipeline';

-- =====================================================
-- TABLE: TICKET_HISTORY (audit trail)
-- =====================================================
CREATE TABLE IF NOT EXISTS ticket_history (
    history_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT NOT NULL,
    action VARCHAR(255) NOT NULL,
    actor_type ENUM('system','agent','customer') DEFAULT 'system',
    actor_id VARCHAR(255),
    detail JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Historique tickets';

-- =====================================================
-- TABLE: AUTOMATION_METRICS (métriques IA)
-- =====================================================
CREATE TABLE IF NOT EXISTS automation_metrics (
    metric_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    ticket_id BIGINT DEFAULT NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value JSON,
    recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticket (ticket_id),
    INDEX idx_metric (metric_name),
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Métriques automatisation';

-- =====================================================
-- VUES UTILES
-- =====================================================

-- Tickets prêts pour auto-résolution
CREATE OR REPLACE VIEW v_actionable_tickets AS
SELECT 
    t.ticket_id, t.subject, t.priority, t.status,
    t.classification_label, t.classification_confidence,
    t.created_at, t.updated_at,
    c.company_name, d.serial_number, pm.model_name
FROM tickets t
LEFT JOIN customers c ON t.customer_id = c.customer_id
LEFT JOIN devices d ON t.device_id = d.device_id
LEFT JOIN printer_models pm ON d.model_id = pm.model_id
WHERE t.status IN ('new','open')
  AND t.classification_confidence >= 0.85
ORDER BY t.priority DESC, t.created_at ASC;

-- Performance pipeline IA
CREATE OR REPLACE VIEW v_pipeline_performance AS
SELECT 
    DATE(t.created_at) as date,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN t.status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved,
    ROUND(AVG(t.classification_confidence), 2) as avg_confidence,
    ROUND(SUM(CASE WHEN t.status = 'auto_resolved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as automation_rate
FROM tickets t
GROUP BY DATE(t.created_at)
ORDER BY date DESC;

-- Messages non traités
CREATE OR REPLACE VIEW v_unprocessed_messages AS
SELECT 
    m.message_id, m.channel, m.direction, m.subject,
    m.received_at, c.company_name
FROM messages m
LEFT JOIN customers c ON m.customer_id = c.customer_id
WHERE m.processed = FALSE
ORDER BY m.received_at ASC;

SET FOREIGN_KEY_CHECKS=1;

-- =====================================================
-- FIN SCHEMA
-- =====================================================
