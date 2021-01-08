from flask import Flask, request, Response
from flask_cors import CORS
import mariadb
import json
import dbcreds

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    if request.method == 'GET':
        print(request.json)
        print(request.args)
        print(request.method)
        login_object = {"loginToken": "123abc"}
        return Response(json.dumps(login_object), mimetype="application/json", status=200)
    elif request.method == 'POST':
        return Response("Created Success!", mimetype="text/html", status=200)

@app.route('/api/login', methods=['GET',])
def login():
    if request.method == 'GET':
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            user_list = cursor.fetchall()
        except Exception as error:
            print("Something went wrong: ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(user_list != None):
                return Response(json.dumps(user_list, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    

@app.route('/api/signup', methods=['POST'])
def signuppage():
        if request.method == 'POST':
            try:
                conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
                cursor = conn.cursor()
                email = input("type email: ")
                username = input("type username: ")
                bio = input("type bio: ")
                birthdate = input("type birthdate: ")
                password = input("type password: ")
                cursor.execute("INSERT INTO user(email, username, bio, birthdate, password) VALUES(?, ?, ?, ?, ?)", [email, username, bio, birthdate, password])
                conn.commit()
                cursor.close()
                conn.close()
            except:
                print("Something went wrong: ")
                print(error)
            finally:
                if(cursor != None):
                    cursor.close()
                if(conn != None):
                    conn.rollback()
                    conn.close()
                return Response(mimetype="application/json", status=201)


@app.route("/api/user", methods=['DELETE'])
def deleteUser():
    if request.method == "DELETE":
        email = request.json.get("email")
        deleteUserSuccess = False

        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            user_list = cursor.fetchall()
            cursor.execute("DELETE FROM user WHERE email =?", [email,])
            conn.commit()
            deleteUserSuccess = True

        except Exception as error:
            print("Something went wrong: ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(deleteUserSuccess):
                return Response(json.dumps({"Message": "The user was deleted!"}, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
