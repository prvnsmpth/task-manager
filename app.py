import web
import json
        
urls = (
    '/events', 'EventHandler'
)
app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

class EventHandler:

    def handle_install(self, event):
        pass
    
    def handle_command(self, event):
        return event['text']

    def POST(self):
        event = json.loads(web.data())

        event_name = event['name']

        if event_name == 'app.install':
            self.handle_install(event)
            return 'OK'
        elif event_name == 'client.slashCommand':
            web.header('Content-Type', 'application/json')
            response = self.handle_command(event)
            json_response = {
                'text': response
            }
            return json.dumps(json_response)

if __name__ == "__main__":
    app.run()
