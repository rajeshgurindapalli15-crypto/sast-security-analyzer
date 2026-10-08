(
echo import os
echo import pickle
echo.
echo API_SECRET_KEY = "sk_live_9876543210123456"
echo.
echo def run_command(user_input):
echo     os.system("ping -c 1 " + user_input)
echo.
echo def get_user(db, user_id):
echo     query = f"SELECT * FROM users WHERE id = '{user_id}'"
echo     db.execute(query)
echo.
echo def load_data(raw_bytes):
echo     return pickle.loads(raw_bytes)
) > tests\sample_vulnerable.py