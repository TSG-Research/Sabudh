from flask import Blueprint, request, session, jsonify,Response
from db_wrapper.Tasks import db_connection
from services.login_services import token
import json
incident = Blueprint('add_incident_', __name__)

@incident.route('/create_incident', methods=['Post'])
def incident_func():
    newReq = request.get_json(force=True)
    username=newReq["username"]
    auth_token=newReq["auth_token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        status = db_connection().add_incident("users", "incidents_table", username, newReq['incident_name'], newReq['place'], newReq['description'])
        if status == True:
            data={"status": 200, "info": "Incident created successfully"}
            return Response(json.dumps(data), mimetype='application/json', status=200)
        else:
            data={"status": 400, 'error': status}
            return Response(json.dumps(data), mimetype='application/json', status=400)
    else:
        data={"status": 400, 'error': auth_status}
        return Response(json.dumps(data), mimetype='application/json', status=400)


@incident.route('/edit_incident', methods=['Post'])
def edit_incident():
    newReq = request.get_json()
    username=newReq["username"]
    auth_token=newReq["auth_token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        response = db_connection().edit_incident(newReq)
        if response['status'] == True:
            data={"status": 200, "info": "Incident edited successfully"}
            return Response(json.dumps(data), mimetype='application/json', status=200)
        else:
            data={"status": 400, 'error': response['error']}
            return Response(json.dumps(data), mimetype='application/json', status=400)
    else:
        data={"status": 400, 'error': auth_status}
        return Response(json.dumps(data), mimetype='application/json', status=400)


@incident.route('/show_incidents', methods=['Post'])
def show():
    newReq = request.get_json()
    username = newReq["username"]
    auth_token = newReq["auth_token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        status = db_connection().show_incidents("users", "incidents_table", username)
        if len(status)==0:
            data={"status": 400, 'error': "No Incidences to display"}
            return Response(json.dumps(data), mimetype='application/json', status=400)
        else:
            return jsonify({'status':200,'incidents': [dict(row) for row in status]})
    else:
        data={"status": 400, 'error': auth_status}
        return Response(json.dumps(data), mimetype='application/json', status=400)

@incident.route('/delete_incident', methods=['Post'])
def delete():
    newReq = request.get_json()
    username = newReq["username"]
    auth_token = newReq["auth_token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        response = db_connection().delete_incident(incident_id=newReq['incident_id'],user_id=newReq['user_id'])
        if response['query_status'] ==True:
            data={"status": 200, 'info': "Incident deleted successfully"}
            return Response(json.dumps(data), mimetype='application/json', status=200)
        else:
            data={'status':400,'error':response['error']}
            return Response(json.dumps(data), mimetype='application/json', status=400)
    else:
        data={"status": 400, 'error': auth_status}
        return Response(json.dumps(data), mimetype='application/json', status=400)
