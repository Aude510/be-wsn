import datetime
import hashlib

import mysql.connector
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template

host = "129.151.225.70"
user = "mamie"
password = "your_password_here"
database = "MamieDB"


connexion_mamie_db = None
mamie_db = None

def connect_to_database():
    global connexion_mamie_db, mamie_db
    try:
        connexion_mamie_db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        mamie_db = connexion_mamie_db.cursor()
        print("Connected to the database")
    except Exception as e:
        print(f"Error: {e}")


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '57I7IU8hihuityuioIUY8OKKIUJjhgfdertyujaqwxcvbFLDSKFNSKNGKJKSKNjkpghlkJHJkjhGHJjGJfhjruikYUKRTetrhJBkjvxddZè'  # Changez ceci pour une clé secrète réelle



# Endpoint to get all tasks
@app.route('/test', methods=['GET'])
def get_tasks():
    return "Mamie pas encore morte"


# Endpoint to get a specific task by ID
@app.route('/test/<int:test_id>', methods=['GET'])
def get_task(test_id):
    return "Mamie morte dans " + str(test_id) + " jours"


# Endpoint to create a new task
@app.route('/test', methods=['POST'])
def create_task():
    return "OK"


@app.route('/mamie-debout', methods=['POST'])
def insert_debout():
    global connexion_mamie_db, mamie_db
    debout = request.json.get('debout')
    debout = int(debout)

    try:
        query = "INSERT INTO Mamie_debout (date_heure, debout) VALUES (NOW(), %s);"
        mamie_db.execute(query, (debout,))
        connexion_mamie_db.commit()
        return "OK, reçu"
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
           e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
           e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            print("Connection lost. Reconnecting...")
            connect_to_database()
            mamie_db.execute(query, (debout,))
            connexion_mamie_db.commit()
            return "OK, reçu after reconnect"
        else:
            return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


@app.route('/mamie-asphyxie', methods=['POST'])
def insert_asphyxie():
    global connexion_mamie_db, mamie_db
    asphyxie = request.json.get('asphyxie')
    asphyxie = float(asphyxie)

    try:
        query = "INSERT INTO Mamie_asphyxie (date_heure, asphyxie) VALUES (NOW(), %s);"
        mamie_db.execute(query, (asphyxie,))
        connexion_mamie_db.commit()
        return "OK, reçu"
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
           e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
           e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            print("Connection lost. Reconnecting...")
            connect_to_database()
            mamie_db.execute(query, (asphyxie,))
            connexion_mamie_db.commit()
            return "OK, reçu after reconnect"
        else:
            return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"


@app.route('/mamie-debout', methods=['GET'])
def get_mamie_debout():
    try:
        query = "SELECT * FROM Mamie_debout ORDER BY date_heure DESC LIMIT 1;"
        mamie_db.execute(query)
        result = mamie_db.fetchone()
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
                e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
                e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            print("Connection lost. Reconnecting...")
            connect_to_database()
            mamie_db.execute(query)
            result = mamie_db.fetchone()

    if type(result) == tuple:
        if result[2] == 1:
            return render_template('grandmafine.html')
        else:
            return render_template('grandmafell.html')
    else:
        return 0

@app.route('/mamie-asphyxie', methods=['GET'])
def get_mamie_asphyxie():
    try:
        query = "SELECT * FROM Mamie_asphyxie ORDER BY date_heure DESC LIMIT 1;"
        mamie_db.execute(query)
        result = mamie_db.fetchone()
    except mysql.connector.Error as e:
        if e.errno == mysql.connector.errorcode.CR_SERVER_GONE_ERROR or \
                e.errno == mysql.connector.errorcode.CR_SERVER_LOST or \
                e.errno == mysql.connector.errorcode.ER_CON_COUNT_ERROR:
            print("Connection lost. Reconnecting...")
            connect_to_database()
            mamie_db.execute(query)
            result = mamie_db.fetchone()

    if type(result) == tuple:
        if result[2] > 1:
            return render_template('grandmadead.html')
        else:
            return render_template('grandmafine.html')
    else:
        return 0



connect_to_database()

if __name__ == '__main__':
    app.run(host='10.8.0.4', port = 9443)
