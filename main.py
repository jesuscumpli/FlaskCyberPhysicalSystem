from flask import Flask
from routes import *

app = Flask(__name__)
app.register_blueprint(routes)
app.secret_key = '6ee9a71761572d9f91dc2067da170889'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

