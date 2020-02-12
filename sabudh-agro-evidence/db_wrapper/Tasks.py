# import sys
# sys.path.append('../')
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, func
from config import DATABASE_IP, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME
import pandas as pd
from flask import jsonify
# from services.login_services import hash

class db_connection():
    def __init__(self):
        self.engine = create_engine("mysql+mysqlconnector://{0}:{1}@{2}/{3}".format(DATABASE_USERNAME, DATABASE_PASSWORD,\
                                                                                 DATABASE_IP, DATABASE_NAME))

        # self.engine = create_engine("mysql+mysqldb://root@127.0.0.1:3306/test_api")
    def sql_to_df(self):
        res = self.engine.execute('select * from customers')
        df = pd.DataFrame(res.fetchall())
        df.columns = res.keys()
        return df

    def create_user(self,tname, newReq,hashed_pwd):
        uname=newReq['username']
        pword=hashed_pwd
        fname=newReq['firstname']
        lname = newReq['lastname']
        age=newReq['age']
        email=newReq['email']
        phone=newReq['phone_num']
        occ=newReq['occupation']
        try:
            query = 'INSERT INTO {} (username,userpassword,firstname,lastname,age,email,phone_num,occupation)\
                       VALUES ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(tname,uname,pword,fname,lname,age,email,phone,occ)
            result=self.engine.execute(query)
            if result:
                return True
        except:
            return False


    def Showall(self):
        result = self.engine.execute('SELECT * FROM users')
        lst = []
        for r in result:
            lst.append(r)
        return lst

    def Showpass(self,username):
        querry = 'SELECT userpassword FROM users WHERE username ="' + str(username) + '";'
        result = self.engine.execute(querry)
        lst = []
        for r in result:
            lst.append(r)
        return lst

    def user_exists(self,username):
        query='SELECT * from users WHERE username = "{}";'.format(username)
        result= self.engine.execute(query)
        result=[res for res in result]
        # print("erw",result)
        if len(result)==0:
            return False
        else:
            return True

    def show_assets_list(self, tname1, tname2, uname):
        #done = False

        '''
        The code to show assets to the user
        '''
        try:
            #result = self.engine.execute('select * from ' + str(tname))
            query = "select asset_url from " + str(DATABASE_NAME) + "." + str(tname2) + \
                    " JOIN assets_list ON " + str(tname2) + ".id=" + str(tname1) + ".id where username='"+str(uname)+"'"
            result = self.engine.execute(query)
            final_result = []
            for res in result:
                final_result.append(res)
            if len(final_result) == 0:
                return "No Result Found"
            else:
                return final_result
        #
        except:
            return "Connection not created or table does not exist"

    def upload_url(self, tname1, tname2, uname, file_url):
        query = "Insert into " + str(DATABASE_NAME) + "." + str(tname2) + " (id, asset_url) VALUES ((select id from " +\
                    str(DATABASE_NAME) + "." + str(tname1) + " where username='" + str(uname) + "'),'" + str(file_url) + "')"

        print(tname1)

        # query = 'INSERT INTO ' + str(tname2) + ' (id,asset_url)' + 'VALUES ((select id from "' + str(DATABASE_NAME) + '.' \
        #         + str(tname1) + '" where username = "' + str(uname) + '"), "' + str(file_url) + '")"'

        try:
            self.engine.execute(query)
        # if result:
            return "Successfully Uploaded"

        except Exception as e:
            return "Try again"
        # else:
        # return "Try again"


    def add_incident(self,tname1, tname2, uname, incident_name, place, description):
        query = "Insert into " + str(DATABASE_NAME) + "." + str(tname2) + " (user_id, incident_name, place, description, timestamp)" \
                " VALUES ((select id from " + str(DATABASE_NAME) + "." + str(tname1) + " where username='" + \
                str(uname) + "'),'" + str(incident_name) + "', '" + str(place) + "', '" + str(description) + "', CURRENT_TIMESTAMP)"

        try:
            self.engine.execute(query)
            return True
        except IntegrityError:
            return "Incorect username"

    def show_incidents(self, tname1, tname2, uname):
        result = self.engine.execute("SELECT * FROM "+str(tname2)+" where user_id=(select id from "+str(tname1)+
                                     " where username='"+str(uname)+"')")
        lst = []
        for r in result:
            lst.append(r)
        return lst

    def show_profile(self,username):
        query="SELECT * FROM users where username = '{}'".format(username)
        res = self.engine.execute(query)
        df = pd.DataFrame(res.fetchall())
        df.columns = res.keys()
        return df.to_dict(orient='records')

    def edit_profile(self,newReq):
        try:
            for key,value in zip(newReq.keys(),newReq.values()):
                if key in ['token','id','username','userpassword']:
                    continue
                query= 'UPDATE users set {}="{}" WHERE username="{}"'.format(key,value,newReq['username'])
                self.engine.execute(query)
            return {'status':True}
        except:
            return {"status":False,"error":"wrong username or unidentified field in user profile"}

    def edit_incident(self, newReq):
        try:
            for key, value in zip(newReq.keys(), newReq.values()):
                if key in ["description","incident_name","place"]:
                    query = 'UPDATE incidents_table set {}="{}" WHERE user_id={} and incident_id={}'.format(
                        key, value, newReq['user_id'],newReq['incident_id'])
                    self.engine.execute(query)
            return {'status': True}
        except:
            return {"status": False, "error": "wrong username or unidentified field encountered during updating incident"}

    def version(self,version_id):
        query= "SELECT * from version where version_id={}".format(version_id)
        try:
            result=self.engine.execute(query)
            # print('::;',result)
            if result:
                df = pd.DataFrame(result.fetchall())
                df.columns = result.keys()
                df_dict=df.to_dict(orient='records')
                return {"query_status":True,"data":df_dict}
        except:
            return {"query_status":False,"error":"data does not exist or could not connect to database"}


    def delete_incident(self,incident_id,user_id):
        query = "DELETE from incidents_table where incident_id={} and user_id={}".format(incident_id,user_id)
        try:
            result = self.engine.execute(query)
            if result:
                return {"query_status": True}
        except:
            return {"query_status": False, "error": "incorrect incident_id or user_id, or could not connect to database"}
