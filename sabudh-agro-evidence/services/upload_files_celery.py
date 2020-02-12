# import sys

# sys.path.insert(0, '/home/mandy/Desktop/sabudh_agro_evidence/services')
# sys.path.append('../')
# sys.path.append('../')

from celery import Celery
from flask import session
from db_wrapper.Tasks import db_connection
import boto3
from boto3.s3.transfer import S3Transfer

celery = Celery(broker='redis://localhost:6379',
                backend='redis://localhost:6379')  # initializing the celery


@celery.task(name='upload_file_app_celery', bind=True)
def upload_file(self, filename):
    # if session['logged_in']:
    path = '/home/mandy/Desktop/' + str(filename)  # path to where we saved the temporary files in the flask file

    path_save = '/home/mandy/sabudh/' + str(filename)

    ''' Here the s3 upload file code will be written and the below code can be commented because we know the path
    and we can directly pick that file to upload in the server(s3) '''

    ''' This code can be omitted'''
    '''It is used to save the file locally'''
    with open(path, 'rb') as file:
        data = file.read()	#read the file

    with open(filename, 'wb') as f:
        f.write(data)	#save the file where we want to

    file.close()
    f.close()

    '''The below code uploads the file to s3 bucket and find the object url uploaded'''

    # credentials = {
    #     'aws_access_key_id': aws_access_key_id,
    #     'aws_secret_access_key': aws_secret_access_key
    # }
    #
    # client = boto3.client('s3', 'us-west-2', **credentials)
    # transfer = S3Transfer(client)
    #
    # transfer.upload_file(path, bucket, key, extra_args={'ACL': 'public-read'})
    #
    # file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key)

    '''
    The below code writes that url to the table
    '''
    file_url = "vdjb@jrbg@hkg"
    # db_connection().upload_url("new_table", "assets_list", str(username), str(file_url))

    return str(file_url)

    # else:
    #     return "Login First"
