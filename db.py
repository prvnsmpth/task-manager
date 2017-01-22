import sqlite3


class DB:

    def __init__(self, db_name):
        self.name = db_name
        self.conn = sqlite3.connect(db_name)

    def create_user(user_id):
        try:
            with self.conn:
                t = (user_id,)
                self.conn.execute("INSERT INTO users VALUES (?)", t)
        except sqlite3.IntegrityError:
            print 'User', user_id, 'already exists, skipping'


