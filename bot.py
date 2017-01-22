from pyflock import FlockClient, Message

CONF_RESP = "OK! I'll reach out to your team members and get back to you soon!"

STATUS_Q = """
    Hi {0}! This is your friendly neighbourhood task bot!
    Just wanted to check in on what you're working on right now.
"""

class Bot:

    def __init__(self, bot_token, app_id, db):
        self.app_id = app_id
        self.db = db
        self.bot_token = bot_token

    def send_simple_msg(self, sender_id, msg):
        flock_client = FlockClient(token=self.bot_token, app_id=self.app_id)
        flock_client.send_chat(Message(to=sender_id, text=msg))

    def notify_group_members(self, group_id):
        flock_client = FlockClient(token=self.bot_token, app_id=self.app_id)

        for member in flock_client.get_group_members():
            self.send_simple_msg(member['id'], STATUS_Q)

    def handle(self, msg):
        sender_id = msg['from']
        message = msg['text']

        if message == 'updates':
            user_token = self.db.get_user_token(sender_id)

            # Fetch all the user's groups
            flock_client = FlockClient(token=user_token, app_id=self.app_id)
            groups = flock_client.get_groups()

            self.send_simple_msg(CONF_RESP)

            self.notify_group_members(groups[0]['id'])
