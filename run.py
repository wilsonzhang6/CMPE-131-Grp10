'''
#provided by teach
#starts the entire website
from app import app
app.run(threaded=true)
'''

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

