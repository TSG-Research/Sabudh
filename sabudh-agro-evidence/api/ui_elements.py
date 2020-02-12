from flask import Blueprint, request, session, jsonify,Response
from db_wrapper.Tasks import db_connection
from services.login_services import token
import json
ui_app = Blueprint('ui_elements', __name__)

@ui_app.route('/version', methods=['Post'])
def version():
    newReq = request.get_json()
    try:
        version_id=newReq['version_id']
        response_data = db_connection().version(version_id)
        if response_data['query_status'] == True:
            data={'status':200,'data':response_data['data']}
            return Response(json.dumps(data), mimetype='application/json', status=200)
        else:
            data={'status':400,'data':response_data['error']}
            return Response(json.dumps(data), mimetype='application/json', status=400)
    except:
        data={'status':400,"error":"missing parameters"}
        return Response(json.dumps(data),mimetype='application/json', status=400)


