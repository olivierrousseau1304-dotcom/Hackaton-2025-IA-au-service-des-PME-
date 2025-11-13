-- =====================================================
-- SCHÉMA MYSQL - SUPPORT CLIENT IA
-- Compatible MySQL 5.7+
-- =====================================================
-- Importer ce fichier dans MySQL:
-- mysql -u username -p database_name < schema.sql
-- =====================================================

-- =====================================================
-- TABLE: CLIENTS
-- =====================================================
CREATE TABLE IF NOT EXISTS clients (
    client_id VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telephone VARCHAR(20),
    entreprise VARCHAR(255),
    type_licence VARCHAR(100),
    niveau_technique ENUM('debutant', 'moyen', 'avance') DEFAULT 'moyen',
    nombre_tickets_total INT DEFAULT 0,
    nombre_tickets_resolus_auto INT DEFAULT 0,
    taux_satisfaction FLOAT,
    derniere_interaction DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: TICKETS
-- =====================================================
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    client_id VARCHAR(20),
    channel ENUM('email', 'sms', 'phone') NOT NULL,
    subject TEXT NOT NULL,
    content LONGTEXT NOT NULL,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    status ENUM('new', 'auto_resolved', 'escalated', 'in_progress', 'resolved', 'closed') DEFAULT 'new',
    auto_resolvable BOOLEAN DEFAULT FALSE,
    confidence_score FLOAT,
    resolution_type VARCHAR(100),
    resolution_applied TEXT,
    estimated_resolution_time VARCHAR(50),
    actual_resolution_time INT,
    assigned_to VARCHAR(100),
    escalated BOOLEAN DEFAULT FALSE,
    escalation_reason TEXT,
    client_rating INT,
    client_feedback TEXT,
    knowledge_base_ref VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE SET NULL,
    INDEX idx_client_id (client_id),
    INDEX idx_status (status),
    INDEX idx_category (category),
    INDEX idx_created_at (created_at),
    INDEX idx_priority (priority),
    INDEX idx_confidence_score (confidence_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: RESOLUTIONS (Base de connaissance)
-- =====================================================
CREATE TABLE IF NOT EXISTS resolutions (
    resolution_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    problem_description TEXT NOT NULL,
    solution_title VARCHAR(255) NOT NULL,
    solution_steps JSON,
    solution_full_text LONGTEXT,
    success_rate FLOAT,
    times_used INT DEFAULT 0,
    average_resolution_time INT,
    knowledge_base_ref VARCHAR(50) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_kb_ref (knowledge_base_ref),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: TICKET_HISTORY (Audit trail)
-- =====================================================
CREATE TABLE IF NOT EXISTS ticket_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id VARCHAR(20),
    action VARCHAR(100) NOT NULL,
    action_by VARCHAR(100),
    action_details JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    INDEX idx_ticket_id (ticket_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABLE: AUTOMATION_METRICS (Monitoring IA)
-- =====================================================
CREATE TABLE IF NOT EXISTS automation_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    total_tickets INT DEFAULT 0,
    auto_resolvable_tickets INT DEFAULT 0,
    auto_resolved_tickets INT DEFAULT 0,
    avg_confidence_score FLOAT,
    avg_resolution_time INT,
    automation_rate FLOAT,
    escalation_rate FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_date (date),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- VUE: Tickets non résolus
-- =====================================================
CREATE OR REPLACE VIEW v_unresolved_tickets AS
SELECT 
    t.ticket_id,
    t.subject,
    t.priority,
    t.category,
    t.confidence_score,
    t.status,
    t.created_at,
    c.client_id,
    c.nom,
    c.prenom
FROM tickets t
LEFT JOIN clients c ON t.client_id = c.client_id
WHERE t.status IN ('new', 'in_progress', 'escalated')
ORDER BY t.priority DESC, t.created_at ASC;

-- =====================================================
-- VUE: Performance d'automatisation
-- =====================================================
CREATE OR REPLACE VIEW v_automation_performance AS
SELECT 
    DATE(t.created_at) as date,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN t.auto_resolvable THEN 1 ELSE 0 END) as auto_resolvable_count,
    SUM(CASE WHEN t.status = 'auto_resolved' THEN 1 ELSE 0 END) as auto_resolved_count,
    ROUND(AVG(t.confidence_score), 2) as avg_confidence,
    ROUND(SUM(CASE WHEN t.status = 'auto_resolved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as automation_rate
FROM tickets t
GROUP BY DATE(t.created_at)
ORDER BY date DESC;

-- =====================================================
-- FIN - Schéma MySQL
-- =====================================================
