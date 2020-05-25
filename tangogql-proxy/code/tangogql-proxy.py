import requests
import json
import sys
from time import sleep
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

login_url = 'http://192.168.93.61:31822/login'
tangogql_url = 'http://192.168.93.61:30608/db'

def login(username, password):
    jsonLogin={"username":username,"password":password}
    r = requests.post(url=login_url, json=jsonLogin)
    return r.cookies.get_dict()['webjive_jwt']

@app.route('/mutation', methods=['POST'])
def mutation():
    app.logger.info(request.values)
    app.logger.info(request.data)
    jsonInput = json.loads(request.data)
    app.logger.info(json.dumps(jsonInput))
    app.logger.info(jsonInput['username'])
    app.logger.info(jsonInput['password'])
    app.logger.info(jsonInput['mutation'])
    cookies = {'webjive_jwt': login(jsonInput['username'],jsonInput['password'])}
    r = requests.post(url=tangogql_url, json=json.loads(jsonInput['mutation']), cookies=cookies)
    app.logger.info("response from tangogql=" + r.text)
    response = app.response_class(
        response=json.dumps(json.loads(r.text)),
        status=200,
        mimetype='application/json'
    )
    return response
