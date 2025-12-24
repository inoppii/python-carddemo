import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting to {DATABASE_URL}")
try:
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
    print("Success!")
    conn.close()
except Exception as e:
    print(f"Failed: {e}")
