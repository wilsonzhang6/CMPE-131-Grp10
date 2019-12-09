'''
#provided by teach
#starts the entire website
from app import app
app.run(threaded=true)
'''

from app import create_app
from flask_mail import Mail

app = create_app()
mail = Mail(app)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

