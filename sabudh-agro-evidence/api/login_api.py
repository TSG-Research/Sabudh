from flask import request, jsonify,Blueprint,Response, session
from db_wrapper.Tasks import db_connection
from services.login_services import hash
import json
login_app = Blueprint('login',__name__)

@login_app.route('/create_user',methods = ['POST'])
def insertDb():
    newReq = request.get_json(force=True)
    hashed_pwd=hash().genHash(newReq['userpassword'])

    try:
        status=db_connection().user_exists(newReq['username'])
        if status:
            data={"status":400,'error':"username already exist"}
            return Response(json.dumps(data), mimetype='application/json', status=400)
        else:
            result=db_connection().create_user('users',newReq,hashed_pwd)
            if result==True:
                data={"status":200,"info":"user created successfully"}
                return Response(json.dumps(data), mimetype='application/json', status=200)
            else:
                data = {"status": 400, "error": "could not create new user"}
                return Response(json.dumps(data), mimetype='application/json', status=400)
    except :
        data={"status":400,"error":"could not create new user"}
        return Response(json.dumps(data), mimetype='application/json', status=400)

@login_app.route('/login',methods = ['POST'])
def checkPass():
    newReq = request.get_json(force=True)
    try:
        status = db_connection().user_exists(newReq['name'])
        if status:
            verification_result = hash().verifyPassword(UsrName=newReq['name'], Pwd=newReq['password'])
            if verification_result["status"] == 200:
                data = {"status": verification_result["status"], "token": verification_result['token'].decode('utf-8'),
                        "username": newReq['name']}
                return Response(json.dumps(data), mimetype='application/json', status=200)
            else:
                data = {"status": verification_result["status"], "error": verification_result["error"]}
                return Response(json.dumps(data), mimetype='application/json', status=400)
        else:
            data = {"error": "User did not exists","status":400}
            return Response(json.dumps(data), mimetype='application/json', status=400)
    except :
        data={"error":"could not login","status":400}
        return Response(json.dumps(data), mimetype='application/json', status=400)





