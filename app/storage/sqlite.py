import os, sqlite3

def get_conn(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS outbound_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now')),
        to_addr TEXT,
        body TEXT,
        provider_sid TEXT,
        status TEXT
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inbound_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now')),
        from_addr TEXT,
        to_addr TEXT,
        body TEXT,
        raw TEXT
    );""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS status_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT (datetime('now')),
        message_sid TEXT,
        status TEXT,
        error_code TEXT,
        raw TEXT
    );""")
    conn.commit()

def insert_outbound(conn, to_addr, body, provider_sid, status):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO outbound_messages (to_addr, body, provider_sid, status) VALUES (?,?,?,?)",
        (to_addr, body, provider_sid, status),
    )
    conn.commit()
    return cur.lastrowid

def insert_inbound(conn, from_addr, to_addr, body, raw):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO inbound_messages (from_addr, to_addr, body, raw) VALUES (?,?,?,?)",
        (from_addr, to_addr, body, raw),
    )
    conn.commit()
    return cur.lastrowid

def insert_status(conn, message_sid, status, error_code, raw):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO status_events (message_sid, status, error_code, raw) VALUES (?,?,?,?)",
        (message_sid, status, error_code, raw),
    )
    conn.commit()
    return cur.lastrowid
