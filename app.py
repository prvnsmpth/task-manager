import web
        
urls = (
    '/hello', 'hello',
    '/events', 'EventHandler'
)
app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

class EventHandler:

    def POST(self):
        data = web.input()
        print 'User ID', data
        return 'OK'

if __name__ == "__main__":
    app.run()
