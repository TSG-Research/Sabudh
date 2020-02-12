from flask import Blueprint, jsonify, session,request,Response
from db_wrapper.Tasks import db_connection
from services.login_services import token
import json
show_incident = Blueprint('show_incident_', __name__)
#
# @show_incident.route('/show_incidents', methods=['Post'])
# def show():
#     newReq = request.get_json()
#     username = newReq["username"]
#     auth_token = newReq["auth_token"]
#     auth_status = token().authenticate_token(auth_token)
#     if auth_status == True:
#         status = db_connection().show_incidents("users", "incidents_table", username)
#         if len(status)==0:
#             data={"status": 400, 'error': "No Incidences to display"}
#             return Response(json.dumps(data), mimetype='application/json', status=400)
#         else:
#             return jsonify({'status':200,'incidents': [dict(row) for row in status]})
#     else:
#         data={"status": 400, 'error': auth_status}
#         return Response(json.dumps(data), mimetype='application/json', status=400)