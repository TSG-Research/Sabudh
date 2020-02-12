from flask import Blueprint, jsonify, session,request,Response
from db_wrapper.Tasks import db_connection
from services.login_services import token
import json
user_profile_app = Blueprint('profile_app', __name__)

@user_profile_app.route('/show_user_profile', methods=['Post'])
def show():
    newReq = request.get_json()
    username = newReq["username"]
    auth_token = newReq["auth_token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        # try:
        data = db_connection().show_profile(username)
        result={"status":200,"data":data}
        return Response(json.dumps(result), mimetype='application/json', status=200)
        # except:
        #     data={"status":400,"error":"could not show user details"}
        #     return Response(json.dumps(data), mimetype='application/json', status=400)
    else:
        data={"status": 400, 'error': auth_status}
        return Response(json.dumps(data), mimetype='application/json', status=400)

@user_profile_app.route('/edit_user_profile', methods=['Post'])
def edit():
    newReq = request.get_json()
    username = newReq["username"]
    auth_token = newReq["token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        response = db_connection().edit_profile(newReq)
        if response['status'] ==True:
            data={"status":200,"info":"profile edited successfully"}
            return Response(json.dumps(data), mimetype='application/json', status=200)
        else:
            data={"status":400,"error":response['error']}
            return Response(json.dumps(data), mimetype='application/json', status=400)
    else:
        data={"status": 400, 'error': auth_status}
        return Response(json.dumps(data), mimetype='application/json', status=400)