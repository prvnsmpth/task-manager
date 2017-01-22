from pyflock import FlockClient, Message, Attachment, Views

CONF_RESP = "OK! I'll reach out to your team members and get back to you soon!"

STATUS_Q = """
Hi {0}! This is your friendly neighbourhood TaskManager bot!
Just wanted to check in on what you're working on right now.
"""
ETA_Q = """
OK! How long do you think that will take?
"""
FINAL_RESP = """
Great, thanks for the update! Have a good day :)
"""
STATUS_REPORT = "Hi! I'm done fetching status updates from everyone. Here's what I got:"

class Bot:

    def __init__(self, bot_token, app_id, db):
        self.app_id = app_id
        self.db = db
        self.bot_token = bot_token

    def send_simple_msg(self, recipient_id, msg, attachments=None):
        flock_client = FlockClient(token=self.bot_token, app_id=self.app_id)
        flock_client.send_chat(Message(to=recipient_id, text=msg, attachments=attachments))

    def notify_group_members(self, sender_id, members):
        notified = 0
        for member in members:
            if member['id'] != sender_id:
                self.send_simple_msg(member['id'], STATUS_Q.format(member['firstName']))
                notified += 1
        return notified
    
    def get_group_members(self, user_token, group_id):
        flock_client = FlockClient(token=user_token, app_id=self.app_id)
        return flock_client.get_group_members(group_id)
    
    def create_empty_updates(self, sender_id, request_id, members):
        for member in members:
            if member['id'] != sender_id:
                self.db.create_empty_update(request_id, member)

    def send_report(self, request_id):
        views = Views()
        responses = self.db.fetch_all_responses(request_id)
        report = '<br/>'.join(["<b>{0}</b><br/><b>Task</b>: {1}<br/><b>ETA</b>: {2}<br/>"
            .format(res['responder'], 
                res['responses'][0], res['responses'][1]) for res in responses])
        views.add_flockml("<flockml>{0}</flockml>".format(report))
        attachment = Attachment(title='Status Report', description='Your team\'s status updates for today', views=views)
        requestor_id = self.db.get_requestor(request_id)
        self.send_simple_msg(requestor_id, STATUS_REPORT, attachments=[attachment])

    def handle(self, msg):
        sender_id = msg['from']
        message = msg['text']

        if message == 'updates':
            user_token = self.db.get_user_token(sender_id)
            self.send_simple_msg(sender_id, CONF_RESP)

            # Fetch all the user's groups, notify first one
            flock_client = FlockClient(token=user_token, app_id=self.app_id)
            groups = flock_client.get_groups()
            first_group = groups[0]

            members = self.get_group_members(user_token, first_group['id'])
            notified = self.notify_group_members(sender_id, members)
            request_id = self.db.create_su_request(sender_id, notified)
            self.create_empty_updates(sender_id, request_id, members)
        else:
            num_responses, request_id = self.db.add_response(sender_id, message)
            if num_responses >= 2:
                response = FINAL_RESP
                self.db.mark_complete(sender_id)
            elif num_responses == 1:
                response = ETA_Q

            self.send_simple_msg(sender_id, response)

            num_left = self.db.fetch_remaining(request_id)
            if num_left == 0:
                self.send_report(request_id)
