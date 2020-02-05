#!/usr/bin/env/python3.6
from flask import Flask, request, redirect, url_for, Markup, make_response 
from flaskext.mysql import MySQL
from jinja2 import Environment, FileSystemLoader
import subprocess


app = Flask(__name__)
loader = FileSystemLoader( searchpath="templates/" )
env = Environment(loader=loader)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_SOCKET'] = None


mysql = MySQL()
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        name = details['name']
        phrase = details['phrase']
        conn = mysql.get_db()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MyPhrases ("
                            "id INT NOT NULL AUTO_INCREMENT,"
                            "PRIMARY KEY(id),"
                            "name    VARCHAR(100),"
                            "phrase  VARCHAR(100))")
        cursor.execute("INSERT INTO MyPhrases(name, phrase) VALUES (%s, %s)", (name, phrase))
        conn.commit()
        cursor.close()
        return redirect('/phrases')
        
    # return "Hello world!"
    template = env.get_template('index.html')
    return make_response(template.render())


@app.route('/phrases')
def show_all_phrases():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MyPhrases")
    data = cursor.fetchall()
    cursor.close()
    template = env.get_template('phrases.html')
    return make_response(template.render(data=data))    


@app.route('/hello/<name>')
def hello(name):
    template = env.get_template('greetings.html')
    js_url = url_for('static', filename='add.js')
    return make_response(template.render(name=name,js_url=js_url))     


@app.route('/bin', methods=['GET', 'POST'])
def binary_file():
    if request.method == "POST":        
        args = ("gcc","static/script.c", "-o","static/binary_file")
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()

    args = ("static/binary_file")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output


# The host='0.0.0.0' means the web app will be accessible to any device on the network
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
