import web
import json
import sqlite3
from db import DB
from bot import Bot

from pyflock import FlockClient, Message
        
urls = (
    '/hello', 'Hello',
    '/events', 'EventHandler'
)
app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

# Flock client
bot_token = 'ce1e2893-8306-4574-8f29-522aa3d20439'
app_id = 'a643fd2c-326e-462f-879a-f49ddc019f2b'
flock_client = FlockClient(token=bot_token, app_id=app_id)

# Database client
db = DB('db.sqlite3')

bot = Bot(bot_token, app_id, db)

class EventHandler:

    def handle_install(self, event):
        db.create_user(event)
    
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
            bot.handle(event['message'])


class Hello:

    def GET(self):
        return 'OK'

if __name__ == "__main__":
    app.run()
