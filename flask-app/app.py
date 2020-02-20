#!/usr/bin/env/python3.6
import datetime
import json
import secrets
import subprocess

import bcrypt
import jwt
from flask import (Flask, Markup, Request, Response, make_response, redirect,
                   request, url_for)
from flaskext.mysql import MySQL
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
loader = FileSystemLoader(searchpath="templates/")
env = Environment(loader=loader)

#Cambiar esta parte del codigo para cada uno
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Msrccbf99051006360'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = "db_ecommerce"
app.config['MYSQL_DATABASE_SOCKET'] = None
#--------------------------------------------------------
JWT_KEY = "modwmodwmoddwdsca234"

mysql = MySQL()
mysql.init_app(app)


def invalid_auth_info(info):
    password = info.get("password")
    username = info.get("username")
    return not (username
                and
                password)


def check_cart_info(cart):
    # coupon = cart.get('idCoupon')
    # if not coupon or not isinstance(coupon, str):
    #     return None
    items = cart.get('items')
    if not items or not isinstance(items, dict):
        return None

    for (item_id, item_amount) in items.items():
        try:
            if int(item_id) <= 0 or int(item_amount) <= 0 or int(item_amount) != item_amount:
                raise ValueError
        except:
            return None
    return cart

@app.route('/complete_purchase', methods=['POST'])
def buy_items():
    # user = {'username': 'juan'}
    template = env.get_template('profile.html')
    user = authorize_and_get_user(request)
    if not user:
        return
    
    # cart = {'items': {'1': 200, '2': 1}}
    cart = check_cart_info(request.json)
    if not cart:
        return
    coupon = user['idCoupon']
    _coup = check_coupon_validity(coupon)
    if _coup == None:
        return json.dumps(
                    {"Message": "Cupón Inválido"})
    conn = mysql.connect()
    data = []
    try:
        with conn.cursor() as cursor:
            in_sql = ""
            case_sql = ""
            insert_sql = ""
            case_params = []
            in_params = []
            insert_params = []
            values = {}
            for i_item, (item_id, item_amount) in enumerate(cart['items'].items()):
                item_id = int(item_id)
                case_sql += " WHEN `IdItem`= %s THEN %s "
                in_sql += " %s,"
                case_params.extend([item_id, item_amount])
                in_params.append(item_id)
                #
                if i_item > 0:
                    insert_sql += "UNION ALL SELECT LAST_INSERT_ID(), %s, %s "
                insert_params.extend([item_id, item_amount])
            case_params.extend(in_params)
            in_sql = in_sql[:-1]
            inside = f"""(SELECT (`value` * CASE {case_sql} END) as `valuei`
                        FROM `Item` WHERE `IdItem` IN ({in_sql}))"""
            select_values = """SELECT @purchase_value, @coupon_value;"""

            queries = [("""SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;""", ()),
                       ("""START TRANSACTION;""", ()),
                       (f"""SET @purchase_value = (
                            SELECT SUM(`valuei`) FROM (
                                {inside}
                        ) as `inline_table1` );""", case_params),
                       ("""SET @coupon_value = (
                            SELECT `value` FROM `coupon` WHERE `idcoupon` = %s);""", (coupon, )),
                       (select_values, ()),
                       ("""INSERT INTO `Purchase`(`username`, `value`)
                        SELECT %s, @purchase_value
                        WHERE @purchase_value <= @coupon_value;""", (user['username'], )),
                       (f"""INSERT INTO `Purchase_Item`(`idpurchase`, `iditem`, `amount`)
                            SELECT `a`, `b`, `c` FROM
                                (SELECT LAST_INSERT_ID() as `a`, %s as `b`, %s as `c`
                                {insert_sql}) as `inline_table2`
                            WHERE @purchase_value <= @coupon_value;""", insert_params),
                       ("""UPDATE `coupon` SET `value`=`value`- @purchase_value
                        WHERE `idcoupon`= %s AND @purchase_value <= @coupon_value;
                        """, (coupon,))]
            for (query, params) in queries:
                cursor.execute(query, params)
                if query == select_values:  # SELECT @purchase_value, @coupon_value;
                    values = cursor.fetchone()
                    values = {
                        'purchase_value': values[0], 'coupon_value': values[1]}
                    print(values)
                    if values['purchase_value'] > values['coupon_value']:
                        conn.rollback()
                        return json.dumps(
                            {"Message": f"El costo de la transacción es {values['purchase_value']} y el cupón tiene {values['coupon_value']}.",
                             "success": False
                            })
            data = get_items(cursor, user['username'])
        conn.commit()
        return  make_response(template.render(user=user['username'], coupon=coupon, data_items=data, size=len(data)))
    except Exception as e:
        conn.rollback()
        return json.dumps(
            {"Message": f"Error en la transacción."})


@app.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method != "POST":
        return

    template = env.get_template('index.html')
    info_register = request.form
    info_register = dict(info_register)
    if invalid_auth_info(info_register):
        return
    conn = mysql.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM `User` WHERE `username` = %s;""",
                       info_register["username"])
        data = cursor.fetchall()
        if not data:
            # id_coupon = cursor.lastrowid
            id_coupon = secrets.token_urlsafe(48)
            cursor.execute("""INSERT INTO `coupon`(`idCoupon`, `value`)
                            VALUES (%(id_coupon)s, %(value)s);""",
                           {'id_coupon': id_coupon, 'value': 100})
            hashed_pw = bcrypt.hashpw(
                info_register["password"].encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                """INSERT INTO `User`(`username`, `password`, `idCoupon`)
                    VALUES (%s, %s, %s);""",
                (info_register["username"], hashed_pw, id_coupon))
            conn.commit()

            data = {'coupon':id_coupon}
            response = make_response(template.render(data=data))
            info_register['coupon'] = id_coupon
            create_and_set_jwt(info_register, response)
            return response
        else:
            return make_response(template.render(value="register"))
    except:
        print('fefe')
        return 'dwdw'
    finally:
        cursor.close()
    


def authorize_and_get_user(request: Request):
    token = request.cookies.get("JWT")
    if not token:
        return None
    try:
        decoded = jwt.decode(token, JWT_KEY, verify=True, algorithms='HS256')
        conn = mysql.get_db()
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM `BlackListed_JWT` WHERE `token` = %s;""",
                           token)
            data = cursor.fetchall()
            if len(data) == 0:
                return decoded
    except Exception as e:
        print(e)
    return None


def create_and_set_jwt(user, response: Response):
    if user['password'] is not None:
        user = dict(user)
        del user['password']

    exp = datetime.datetime.utcnow() + datetime.timedelta(days=14)
    encoded_jwt = jwt.encode(
        dict({'exp': exp}, **user), JWT_KEY, algorithm='HS256')
    response.set_cookie(
        "JWT",
        encoded_jwt,
        httponly=True,
        samesite="Lax"
    )


@app.route('/log_out', methods=['POST', 'GET'])
def logout():
    template = env.get_template('login.html')
    response = make_response(template.render(value="login"))

    token = request.cookies.get("JWT")
    if not token:
        return response
    response.set_cookie("JWT", "", expires=0)
    response.delete_cookie("JWT")
    try:
        jwt.decode(
            token, JWT_KEY, verify=True, algorithms='HS256')
        conn = mysql.get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO `BlackListed_JWT`(`token`) VALUES ('%s');""",
                token)
        conn.commit()
    finally:
        return response


@app.route('/log_in', methods=['POST'])
def log_in_2():
    if request.method == "POST":
        info_login = request.form
        if invalid_auth_info(info_login):
            return
        conn = mysql.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """SELECT `username`, `password`, `idCoupon` FROM `User` WHERE 
                `username` = %s;""",
                (info_login['username']))

            user = cursor.fetchone()
            if user:   
                user ={"username":user[0], "password":user[1], "idCoupon": user[2]}
                if bcrypt.checkpw(info_login["password"].encode('utf-8'), user['password']):
                    template = env.get_template('index.html')
                    response = make_response(template.render())
                    create_and_set_jwt(user, response)
                    return response
                else:
                    template = env.get_template('login.html')
                    return make_response(template.render(value="login"))
            else:
                template = env.get_template('login.html')
                return make_response(template.render(value="login"))
        finally:
            cursor.close()

def get_items(cursor, username):
    data = []
    cursor.execute(
            """SELECT `item`.`idItem`, `item`.`name`, `item`.`value` FROM `Purchase` `p` 
            INNER JOIN `Purchase_item`  `pi` ON (`pi`.`idpurchase` = `p`.`idpurchase`)  
            INNER JOIN `item` ON (`pi`.`iditem` = `item`.`idItem`)
            WHERE `p`.`username` = %s;""", username)
    response = cursor.fetchall()
    for item in response:
        data.append({"item": item[1], "quantity": item[2], "value":item[2] })
    return data
    

@app.route('/profile', methods=['GET'])
def purchase_history():
    user = authorize_and_get_user(request)
    if user == None:
        return redirect("/log_in")
    username = user['username']
    conn = mysql.get_db()
    cursor = conn.cursor()
    try:
        data = get_items(cursor, username)

        cursor.execute(
            """SELECT * FROM `User` WHERE `username` = %s;""", username)
        response = cursor.fetchall()
        if not response:
            print("aqui2")
            return redirect("/")
        response = response[0]
        cursor.execute(
            """SELECT * FROM `Coupon` WHERE `idCoupon` = %s;""", response[2])
        response = cursor.fetchall()
        if not response:
            print("aqui1")
            return redirect("/")
        response = response[0]
        template = env.get_template('profile.html')
        return make_response(template.render(user=username, coupon=response[1], data_items=data, size=len(data)))
    finally:
        cursor.close()


def check_coupon_validity(coupon_code):
    args = ("./static/testmysql.exe",
            "localhost",
            app.config['MYSQL_DATABASE_USER'],
            app.config['MYSQL_DATABASE_PASSWORD'],
            app.config['MYSQL_DATABASE_DB'],
            str(app.config['MYSQL_DATABASE_PORT']),
            coupon_code)
    popen = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    popen.wait()

    err = str(popen.stderr.read(), "utf-8")
    if err:
        print("ERROR check_coupon_validity: " + err)
        return None

    output = str(popen.stdout.read(), "utf-8")  # "<couponId> <value> | None"
    if output and output.lower() != "none" and output.strip().count(" ") == 1:
        output = output.split()
        return {"couponId": output[0], "value": int(output[1])}
    else:
        return None


@app.route('/create_tables', methods=['POST'])
def create_tables():
    tables = open("../docs/table_definitions.sql", 'r').read().split(";")
    conn = mysql.get_db()
    cursor = conn.cursor()
    response = json.dumps(
        {"Message": "Las tablas fueron creadas correctamente"})
    try:
        for sql in tables:
            cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()
    return response


@app.route('/drop_tables', methods=['POST'])
def drop_tables():
    drop_tables_query = open("../docs/drop_tables.sql", 'r').read()
    conn = mysql.get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(drop_tables_query)
        conn.commit()
        return json.dumps(
            {"Message": "Las tablas fueron eliminadas correctamente"})
    except:
        return json.dumps(
            {"Message": f"Error: Las tablas no fueron eliminadas."})


@app.route('/', methods=['GET'])
def index():
    template = env.get_template('index.html')
    user = authorize_and_get_user(request) 
    if user != None:
        return make_response(template.render())
    else:
        template = env.get_template('login.html')
        return make_response(template.render(value="login"))


@app.route('/payment', methods=['GET'])
def payment():
    template = env.get_template('payment.html')
    return make_response(template.render())

@app.route('/<path>', methods=['GET', 'POST'])
def login_register(path):
    template = env.get_template('login.html')
    if path == "log_in":
        return make_response(template.render(value="login"))
    elif path == "sign_up":
        return make_response(template.render(value="register"))

#Obtiene los items de la db para pintarlos en el index
@app.route('/getItems', methods=['GET'])
def getItems():
    conn = mysql.get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM `item`""")
        response = cursor.fetchall()
        if response:
            return json.dumps(response)
        else:
            return json.dumps({"Message": "No tiene items"})
    finally:
        cursor.close()

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(error):
    template = env.get_template('not_found.html')
    return make_response(template.render())


# The host='0.0.0.0' means the web app will be accessible to any device on the network
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    # print(check_coupon_validity("coupon1"))
    # print(buy_items(request))
