"""The main application that runs flask server."""

import os
import json
from flask import Flask, request
from src.sensehealth.database_handler import DBHandler
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()
CONFIG = {
    "apiKey": "-none-",
    "serviceAccount": json.loads(os.environ['FIREBASE_API_KEY']),
    "authDomain": "{}.firebaseapp.com".format(os.environ['PROJECT_ID']),
    "databaseURL": "https://{}.firebaseio.com".format(os.environ['PROJECT_ID']),
    "storageBucket": "{}.appspot.com".format(os.environ['PROJECT_ID']),
}
db_handler = DBHandler(CONFIG)


@app.route('/test_frontend', methods=['GET'])
def test_frontend():
    """Testing function for frontend."""
    return json.dumps({"key": "value"})


@app.route('/deposit_data', methods=['POST'])
def deposit_data():
    """Temporary endpoint to print sensor values. Must send JSON Object."""
    data = request.get_json(force=True)
    db_handler.put(['raw_sensor_data'], data, auto_id=True)
    return data


@app.route('/')
def index():
    """Root endpoint. Currently for testing."""
    return "<h1>SenseHealth's Backend</h1>Check out: \
        https://5e9123ecf2fcfcdeef9cb85e--naughty-perlman-a4541f.netlify.com/"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
