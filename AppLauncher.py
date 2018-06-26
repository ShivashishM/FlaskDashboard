import json
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, session, flash
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import os, subprocess
from time import sleep
from threading import Thread
import logging
import csv
from flask_cors import CORS

log_filepath = './'
log_filepath = log_filepath + 'IoCountlog.txt'

logging.basicConfig(#filename=log_filepath,
    filemode='a',
    format='%(asctime)-8s | %(levelname)-6s | %(lineno)4s |%(funcName)15s() | %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
)
app = Flask(__name__)
api = Api(app, prefix="/api")
auth = HTTPBasicAuth()
print(app.config)

CORS(app, allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)

# Our mock database. http://admin:admin@192.168.1.166:5006/api/v1?Date=20180652
USER_DATA = {
    "admin": "admin"
    }

@auth.verify_password
def verify(username, password):
    if not (username and password):
        logging.info("retur non auth")
        return False
    return USER_DATA.get(username) == password

class CounrData(Resource):
    #@auth.login_required
    def get(self):
        try:
            logging.info(request.args)
            if 'Date' in request.args:
                logging.info("PrivateResource3")
                ViewDate = request.args.get('Date')
            filename = ViewDate+"_count.csv"
            csv_rows = []
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                title = reader.fieldnames
                for row in reader:
                    csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
                logging.info(csv_rows)
        except Exception as e:

            return str(e)

        return csv_rows
api.add_resource(CounrData, '/v1')

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def get_background_task_log():
    return "Check API  '/api/v1?Date=yyyymmdd'"

@app.route('/dashboard', methods=['GET'])
@auth.login_required
def get_daskboard():
    return render_template('index.html')
