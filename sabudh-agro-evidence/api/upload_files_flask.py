from db_wrapper.Tasks import db_connection
import sys
from flask import session

# sys.path.insert(0, '/home/mandy/Desktop/sabudh_agro_evidence/services')
sys.path.append('../')
from flask import request, Blueprint
from services.upload_files_celery import upload_file
import os

upload_app = Blueprint('upload_api',__name__)	#creating the flask app (Blueprint)
UPLOAD_FOLDER = '/home/mandy/Desktop/'	#path to temporary save the file(s) from which celery picks up the file to upload in the server

'''
We are temporarily saving the file in the local system because to upload the file to the server we have to know the path of the file.
But when we get any file from flask we get the file only, there is no method to get the filepath.
'''
@upload_app.route("/upload", methods = ['Post'])
# @login_required
def upload_file_flask():

	if session['logged_in']:
		if request.method =='POST':
			file_ = request.files.getlist('upload')	#upload is the key in the form

			if file_:	#if any file exists

				for file in file_:
					print("inside flask")
					file_name = file.filename
					file.save(os.path.join(UPLOAD_FOLDER, file_name))	#save the file to the path given above
					file_url = upload_file.delay(filename = file_name)	#calling celery fuction
					file_url = file_url.get()
					print(file_url)
					db_connection().upload_url("new_table", "assets_list", session['username'], str(file_url))


		return "saved successfully"

	else:
		return "Login First to upload the files"

