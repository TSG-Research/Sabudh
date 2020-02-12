from flask import Blueprint

check=Blueprint('name',__name__)

@check.route('/home')
def home():
    return 'Hi you are inside check api'


# @app.route('/ls')
# def files():
#     s3_resource=boto3.client('s3')
#     data=s3_resource.list_objects_v2(Bucket=S3_BUCKET)
#     return jsonify([entry['Key'] for entry in data['Contents']])
#
# @app.route('/file_upload',methods=['GET','POST'])
# def upload():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'no file'
#         file=request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             # file.save(filename)
#             s3 = boto3.client('s3')
#             s3.upload_file(filename, S3_BUCKET, filename)
#             return 'saved succesfully'
#         else:
#             return 'could not upload'
