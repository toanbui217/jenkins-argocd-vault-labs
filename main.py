from flask import Flask
import os
import psycopg2  # Cho kết nối PostgreSQL
from psycopg2 import OperationalError

app = Flask(__name__)

# Env vars từ Vault injector hoặc env
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'mydb')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'pass')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except OperationalError as e:
        print(f"ERROR: DB connection failed! Details: {e}")
        return None  # Không crash nếu DB fail

# Init table và insert sample data nếu chưa có
def init_db():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS messages
                       (id SERIAL PRIMARY KEY, text TEXT NOT NULL);''')
        # Insert sample nếu table rỗng
        cur.execute("SELECT COUNT(*) FROM messages;")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO messages (text) VALUES ('Hello from DB!');")
        conn.commit()
        cur.close()
        conn.close()

# Fetch messages
def get_messages():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT text FROM messages;")
        messages = cur.fetchall()
        cur.close()
        conn.close()
        return [msg[0] for msg in messages]
    return ["DB connection failed!"]

# Init DB khi app start
init_db()

@app.route('/')
def hello():
    messages = get_messages()
    return f"Hello World! Messages from DB: {', '.join(messages)}"

@app.route('/add')
def add_message():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (text) VALUES ('New message from app!');")
        conn.commit()
        cur.close()
        conn.close()
        return "Message added!"
    return "DB failed!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2307)