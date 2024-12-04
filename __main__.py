from os import abort

import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime
import configparser

# Initiating a Flask application
app = Flask(__name__)

#Read db settings
config = configparser.ConfigParser()
config.read('config.ini')
db_name = config.get('DATABASE', 'db_name')
db_user = config.get('DATABASE', 'db_user')
db_host = config.get('DATABASE', 'db_host')
db_password = config.get('DATABASE', 'db_password')

def connect_db():
    """Return a database connection"""
    return psycopg2.connect(f"host={db_host} dbname={db_name} user={db_user} password={db_password}")

def execute_query(query, params=None, fetchall=False, fetchone=False):
    """Execute a query and optionally fetch one record"""
    try:
        with connect_db() as cnx:
            with cnx.cursor() as db:
                db.execute(query, params or ())
                if fetchall:
                    return db.fetchall()
                if fetchone:
                    return db.fetchone()[0]
                cnx.commit()
                if query.strip().upper().startswith("INSERT"):
                    return db.fetchone()[0]
    except Exception as e:
        raise e

@app.route(rule="/", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        return "This is the GET Endpoint of flask API."

    if request.method == "POST":
        records = execute_query(
            "SELECT * FROM whatsapp_requests;", (), fetchall=True
        )
        response = {'records': records}
        return jsonify(response)

@app.route(rule="/new_interaction", methods=["POST"])
def insert_interaction():
    if request.method == "POST":
        payload = request.get_json()
        try:
            insertion_id = execute_query(
                "INSERT INTO whatsapp_requests (engagement_id, created) VALUES (%s, %s) RETURNING id",
                (payload['engagement_id'], datetime.now())
            )
            return jsonify(insertion_id)
        except Exception as e:
            return f"There was an error: {e}", 500

# Running the API
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
