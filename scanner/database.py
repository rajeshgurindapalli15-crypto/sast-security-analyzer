import sqlite3
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "sast_results.db"

def sync_to_cloud_mongodb(timestamp, target_file, vulnerabilities):
    """Synchronizes scan telemetry to MongoDB Atlas via secure .env configuration."""
    mongo_uri = os.getenv("MONGO_ATLAS_URI")
    if not mongo_uri:
        return  
    
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
        collection.insert_one(document)
    except Exception as e:
        print(f"[-] Warning: Failed to sync telemetry to MongoDB Atlas: {e}")

