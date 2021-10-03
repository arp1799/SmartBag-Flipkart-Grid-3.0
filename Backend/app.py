#loading libraries
from re import X
import joblib
from flask import Flask, request
from main import *
import flask
from flask.json import jsonify

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    x = request.json
    x = x['user_id']
    predictions = call(int(x))
    print(predictions)
    return jsonify({"predictions":predictions[:min(6,len(predictions))]})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
