from flask import request, jsonify,Blueprint,Response, session
from db_wrapper.Tasks import db_connection
# from services.login_services import genHash,verifyPassword
from config import DATABASE_NAME

show_assets_app = Blueprint('asset_list', __name__)
from services.login_services import token

@show_assets_app.route('/show_asset', methods=['Get'])
def show_asset_list():
    done = False

    '''
    The code to show assets to the user
    '''
    newReq = request.get_json()
    username = newReq["username"]
    auth_token = newReq["auth_token"]
    auth_status = token().authenticate_token(auth_token)
    if auth_status == True:
        result = db_connection().show_assets_list("assets_list", "new_table", username)
        print(result)
        return (str(result))
        # else:
        #     return "Login First to list the assets"

