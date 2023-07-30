from typing import List, Dict
import mysql.connector
import json
import os

from app import app

def db_select_jobs() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'employees'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM jobs')
    results = [{_id: _job} for (_id, _job) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route("/")
def index():

    # Use os.getenv("key") to get environment variables
    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"

    return "Hello from Flask"



@app.route('/db')
def index_db() -> str:
    return json.dumps({'db_select_jobs': db_select_jobs()})

