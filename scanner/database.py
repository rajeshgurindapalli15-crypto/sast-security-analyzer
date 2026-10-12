import sqlite3
import os
from datetime import datetime
from pymongo import MongoClient

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

def sync_to_cloud_mongodb(timestamp, target_file, vulnerabilities):
    """Synchronizes scan telemetry to MongoDB Atlas if MONGO_ATLAS_URI is configured."""
    mongo_uri = os.getenv("MONGO_ATLAS_URI")
    if not mongo_uri:
        return  # Gracefully skip cloud sync if offline or unconfigured
    
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        db = client["sast_cloud_telemetry"]
        collection = db["vulnerability_audits"]
        
        document = {
            "scan_timestamp": timestamp,
            "target_file": target_file,
            "total_vulnerabilities": len(vulnerabilities),
            "findings": vulnerabilities
        }
        # Appends a brand-new document on every scan execution
        collection.insert_one(document)
    except Exception as e:
        print(f"[-] Warning: Failed to sync telemetry to MongoDB Atlas: {e}")

def save_vulnerabilities_to_db(target_file, vulnerabilities):
    """Inserts a list of vulnerability dictionaries into local SQLite and syncs to MongoDB Atlas."""
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

    sync_to_cloud_mongodb(timestamp, target_file, vulnerabilities)

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
