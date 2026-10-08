import sqlite3
from datetime import datetime

DB_NAME = "sast_results.db"

def init_db():
    """Initializes the SQLite database and creates the vulnerabilities table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_timestamp TEXT,
            target_file TEXT,
            rule_id TEXT,
            severity TEXT,
            vulnerability TEXT,
            file_line TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_vulnerabilities_to_db(target_file, vulnerabilities):
    """Inserts a list of vulnerability dictionaries into the database."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for vuln in vulnerabilities:
        cursor.execute("""
            INSERT INTO scan_results (scan_timestamp, target_file, rule_id, severity, vulnerability, file_line)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            target_file,
            vuln.get("rule_id"),
            vuln.get("severity"),
            vuln.get("name"),
            str(vuln.get("line"))
        ))
        
    conn.commit()
    conn.close()

def get_scan_history():
    """Retrieves all past scan results from the database."""
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT scan_timestamp, target_file, rule_id, severity, vulnerability, file_line 
        FROM scan_results 
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows