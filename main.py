from flask import Flask
from routes import *
import datetime

app = Flask(__name__)
app.register_blueprint(routes)
app.secret_key = '6ee9a71761572d9f91dc2067da170889'

@app.template_filter()
def format_datetime(date_value):
    date = datetime.datetime.strptime(date_value, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

