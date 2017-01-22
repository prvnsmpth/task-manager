import web
import json
import sqlite3
from db import DB

from pyflock import FlockClient, Message
        
urls = (
    '/events', 'EventHandler'
)
app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

# Flock client
bot_token = '3eaf05be-7d37-4474-bdb5-a1b6f307ed73'
app_id = 'ffc13fc5-ed85-4c04-b52c-d23fda856a3b'
flock_client = FlockClient(token=bot_token, app_id=app_id)

# Database client
db = DB('db.sqlite3')

class EventHandler:

    def handle_install(self, event):
        user_id = event['userId']
        db.create_user(user_id)
    
    def handle_bot_message(self, msg):
        sender_id = msg['from']
        response_msg = Message(to=sender_id, text=msg['text'])
        res = flock_client.send_chat(response_msg)

    def handle_command(self, event):
        pass

    def POST(self):
        event = json.loads(web.data())

        event_name = event['name']

        if event_name == 'app.install':
            self.handle_install(event)
            return 'OK'
        elif event_name == 'client.slashCommand':
            self.handle_command(event)
        elif event_name == 'chat.receiveMessage':
            self.handle_bot_message(event['message'])

if __name__ == "__main__":
    app.run()
