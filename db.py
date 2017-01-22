import psycopg2
from psycopg2 import IntegrityError
import json

DB_HOST = 'ec2-50-17-212-238.compute-1.amazonaws.com'
DB_PORT = 5432
DB_USER = 'evhanutrqdruut'
DB_PASSWORD = 'KlqKZcPIg5dVTFJbtgX90fM_69'
DB_NAME = 'dd70pjvtfenth'

class DB:

    def __init__(self, dbname=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER,
            password=DB_PASSWORD):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password


    def get_conn(self):
        conn = psycopg2.connect("dbname='{0}' host='{1}' port='{2}' user='{3}' password='{4}'"
                .format(self.dbname, self.host, self.port, self.user, self.password))
        return conn

    def create_user(self, user_info):
        with self.get_conn() as conn:
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
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT token FROM users WHERE user_id = %s", (user_id,))
            entry = cur.fetchone()
            cur.close()
            return entry[0] if entry else None

    def get_responses(self, user_id):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT responses FROM status_updates WHERE user_id = %s ORDER BY request_id DESC LIMIT 1", (user_id,))
            row = cur.fetchone()
            cur.close()
            return json.loads(row[0]) if row else None 

    def add_response(self, user_id, response):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT request_id, responses FROM status_updates WHERE responder = %s ORDER BY request_id DESC LIMIT 1", (user_id,))
            row = cur.fetchone()
            cur.close()
            if not row:
                return
            request_id = row[0]
            responses = json.loads(row[1])
            responses.append(response)
            num_responses = len(responses)
            cur = conn.cursor()
            cur.execute("UPDATE status_updates SET responses = %s WHERE request_id = %s AND responder = %s", 
                    (json.dumps(responses), request_id, user_id))
            cur.close()
            return (num_responses, request_id)

    def create_su_request(self, user_id, num_reportees, reportees='all'):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO status_requests (requested_by, requested_of, num_reportees) VALUES (%s, %s, %s) RETURNING id", (user_id, reportees, num_reportees))
            request_id = cur.fetchone()[0]
            cur.close()
            return int(request_id)

    def create_empty_update(self, request_id, member):
        with self.get_conn() as conn:
            cur = conn.cursor()
            user_id = member['id']
            full_name = '{0} {1}'.format(member['firstName'], member['lastName'])
            cur.execute("INSERT INTO status_updates (request_id, responder, full_name, responses, done) VALUES (%s, %s, %s, %s, %s)",
                    (request_id, user_id, full_name, '[]', False))
            cur.close()

    def mark_complete(self, user_id):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT request_id FROM status_updates WHERE responder = %s ORDER BY request_id DESC LIMIT 1", (user_id,))
            row = cur.fetchone()
            if not row:
                return
            request_id = row[0]
            cur = conn.cursor()
            cur.execute("UPDATE status_updates SET done = %s WHERE request_id = %s AND responder = %s", (True, request_id, user_id)) 
            cur.close()

    def fetch_remaining(self, request_id):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM status_updates WHERE request_id = %s and done = %s", (request_id, False))
            row = cur.fetchone()
            if not row:
                return 0
            return row[0]

    def fetch_request_creator(self, request_id):
        with self.get_conn() as conn:
            cur = con.cursor()
            cur.execute("SELECT requested_by FROM status_requests WHERE id = %s", (request_id,))
            row = cur.fetchone()
            if not row:
                return None
            return row[0]

    def fetch_all_responses(self, request_id):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT full_name, responses FROM status_updates WHERE request_id = %s", (request_id,))
            rows = cur.fetchall()

            return [{
                'responder': row[0],
                'responses': json.loads(row[1])
            } for row in rows]

    def get_requestor(self, request_id):
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT requested_by FROM status_requests WHERE id = %s", (request_id,))
            row = cur.fetchone()
            if not row:
                return None
            return row[0]
