#!/usr/bin/env/python3.6
from flask import Flask, request, redirect, url_for, Markup, make_response 
from flaskext.mysql import MySQL
from jinja2 import Environment, FileSystemLoader
import subprocess
from bson.json_util import dumps


app = Flask(__name__)
loader = FileSystemLoader( searchpath="templates/")
env = Environment(loader=loader)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = "db_ecommerce"
app.config['MYSQL_DATABASE_SOCKET'] = None


mysql = MySQL()
mysql.init_app(app)


@app.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == "POST":
        info_register = request.form
        conn = mysql.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM User WHERE username = %s", info_register["username"])
            data = cursor.fetchall()
            if not data:
                user_sql = "INSERT INTO coupon (value) VALUES (%(value)s)"
                data_user = {'value': 100}
                cursor.execute(user_sql, data_user)
                id_coupon = cursor.lastrowid
                user_sql = "INSERT INTO User(username, password, idCoupon) VALUES (%s, %s, %s)"
                cursor.execute(user_sql, (info_register["username"], info_register["password"], id_coupon))
                response = "Fue registrado exitosamente el usuario: %s" % (info_register["username"])
                return dumps(response)
            else:
                response = ("No fue posible registar al usuario: %s" % (info_register["username"]))
                return dumps(response)
        finally:
            conn.commit()
            cursor.close()


@app.route('/log_in/<username>', methods=['GET'])
def log_in(username):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM User WHERE username = %s", username)
        response = cursor.fetchall()
        if response:
            return dumps(response[0])
        else:
            return dumps("No existe el usuario: %s" % (username))
    finally:
        cursor.close()


@app.route('/create_tables', methods=['POST'])
def create_tables():
    tables = open("../docs/Create_Tables.txt", 'r').read().split("|")
    conn = mysql.get_db()
    cursor = conn.cursor()
    response = dumps({"Las tablas fueron creadas correctamente"})
    try:
        for sql in tables:
            cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()
    return response


@app.route('/drop_tables', methods=['POST'])
def drop_tables():
    tables = open("../docs/Drop_Tables.txt", 'r').read().split("|")
    conn = mysql.get_db()
    cursor = conn.cursor()
    response = dumps({"Las tablas fueron eliminadas correctamente"})
    try:
        for sql in tables:
            cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    template = env.get_template('index.html')
    return make_response(template.render())


# The host='0.0.0.0' means the web app will be accessible to any device on the network
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
