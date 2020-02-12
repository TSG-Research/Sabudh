from flask import Flask,jsonify,request
from api.check import check
from api.login_api import login_app
from api.upload_files_flask import upload_app
from api.show_assets_list_api import show_assets_app
from api.logout_api import logout_app
from api.incidents import incident
from api.show_incidents import show_incident
from api.user_profile import user_profile_app
from api.ui_elements import ui_app
from flask_cors import CORS,cross_origin
import flask
import boto3
from werkzeug.utils import secure_filename
from services import upload_files_celery

app = Flask(__name__)
app.secret_key = "super secret key"
CORS(app,)

# app.register_blueprint(check)
app.register_blueprint(login_app)
app.register_blueprint(logout_app)
app.register_blueprint(upload_app)
app.register_blueprint(show_assets_app)
app.register_blueprint(show_incident)
app.register_blueprint(incident)
app.register_blueprint(user_profile_app)
app.register_blueprint(ui_app)


@app.route('/')
def welcome():
    return 'EVIDENCE COLLECTION REST APIs'

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get(
        'Access-Control-Request-Headers', 'Authorization,Origin, X-Requested-With, Content-Type, Accept' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp
if __name__ == "__main__":
    app.run(debug=True,port=80,host="0.0.0.0")
    # app.run(debug=True)