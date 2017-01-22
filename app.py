import web
        
urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
