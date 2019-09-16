from app import app

# different URL the app will implement
@app.route("/")
# called view function
def hello():
    user = {'username': 'Miguel'}
    return '''
	<html>
    <head>
        <title>Home Page - my blog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
	</html>'''
