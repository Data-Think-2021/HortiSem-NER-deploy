from flask import Flask
from flask.helpers import url_for
from flask.json import JSONEncoder
from flask import send_file, request, globals
from flask.views import View

app = Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'foo'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
