import sqlite3

def init():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE users (
            user_id TEXT PRIMARY KEY,
            token TEXT)
    ''')

    cur.execute('''
        CREATE TABLE status_request (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            requested_by TEXT, 
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reportees TEXT)
    ''')

    cur.execute('''
        CREATE TABLE status_response (
            request_id INTEGER,
            responder TEXT,
            type TEXT,
            response TEXT)
    ''')

if __name__ == '__main__':
    init()
