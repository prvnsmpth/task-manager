import sqlite3


class DB:

    def __init__(self, db_name):
        self.name = db_name

    def create_user(self, user_info):
        self.conn = sqlite3.connect(self.name)
        try:
            with self.conn:
                user_id = user_info['userId']
                token = user_info['token']
                t = (user_id, token)
                self.conn.execute("INSERT INTO users VALUES (?,?)", t)
        except sqlite3.IntegrityError:
            print 'User', user_id, 'already exists, skipping'

    def get_user_token(self, user_id):
        self.conn = sqlite3.connect(self.name)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT token FROM users WHERE user_id = ?", (user_id,))
            entry = cur.fetchone()
            return entry['token'] if entry else None

