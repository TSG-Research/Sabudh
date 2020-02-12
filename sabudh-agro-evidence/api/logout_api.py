from flask import request, jsonify,Blueprint,Response, session
# from db_wrapper.Tasks import db_connection

logout_app = Blueprint('logout_', __name__)

@logout_app.route('/logout', methods=['Get'])
def logout():
    try:
        session.pop('username')
        session['logged_in'] = False
        session.pop('secret_key')

        if not session['logged_in']:
            return "Logged out"

        else:
            return "try again"
    except Exception as e:

        return "Error: "+str(e)