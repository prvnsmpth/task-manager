import psycopg2
from psycopg2 import IntegrityError

DB_HOST = 'ec2-50-17-212-238.compute-1.amazonaws.com'
DB_PORT = 5432
DB_USER = 'evhanutrqdruut'
DB_PASS = 'KlqKZcPIg5dVTFJbtgX90fM_69'
DB_NAME = 'dd70pjvtfenth'

class DB:

    def __init__(self, dbname, host, port, user, password):
        self.dbname = dbname or DB_NAME
        self.host = host or DB_HOST
        self.port = port or DB_PORT
        self.user = user or DB_USER
        self.password = password or DB_PASSWORD

    def create_user(self, user_info):
        conn = psycopg2.connect("dbname='{0}' host='{1}' port='{2}' user='{3}' password='{4}'"
                .format(self.dbname, self.host, self.user, self.password))

        with conn:
            try:
                cursor = conn.cursor()
                user_id = user_info['userId']
                token = user_info['token']
                t = (user_id, token)
                cursor.execute("INSERT INTO users VALUES (%s,%s)", t)
                cursor.close()
            except IntegrityError:
                token = self.get_user_token(user_id)
                print 'User', user_id, 'already exists with token', token

    def get_user_token(self, user_id):
        conn = psycopg2.connect("dbname='{0}' host='{1}' user='{2}' password='{3}'"
                .format(self.dbname, self.host, self.user, self.password))
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT token FROM users WHERE user_id = %s", (user_id,))
            entry = cur.fetchone()
            cur.close()
            return entry[0] if entry else None

