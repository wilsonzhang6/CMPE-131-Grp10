from flask import render_template
from app import app

# different URL the app will implement
@app.route("/")
# called view function
def hello():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
