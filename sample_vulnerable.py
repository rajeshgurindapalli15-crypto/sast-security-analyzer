import os
import pickle

API_SECRET_KEY = "sk_live_9876543210123456"

def run_command(user_input):
    os.system("ping -c 1 " + user_input)

def get_user(db, user_id):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    db.execute(query)

def load_data(raw_bytes):
    return pickle.loads(raw_bytes)