import jwt
import datetime
from config import saltKey1,tokenKey
from passlib.hash import  sha512_crypt
from db_wrapper.Tasks import db_connection
from flask import jsonify

class hash():
    def genHash(self,sendString):
        password = str(sendString)
        crypt_obj = sha512_crypt.hash(saltKey1 + password)
        return crypt_obj

    def verifyPassword(self,UsrName,Pwd):
        try:
            hashget = db_connection().Showpass(UsrName)
            if sha512_crypt.verify(saltKey1+Pwd, hashget[0][0]):
                return {"status":200,"token":createToken(UsrName)}
            else :
                return {"status":401,"error":"password does not match"}
        except Exception as e:
            print(e)
            return {"status":400,"error":"db connection error"}

def createToken(usrName):
    token = jwt.encode({'userName' : usrName, 'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30) }, tokenKey)
    return token

class token():
    def createToken(self,usrName):
        token = jwt.encode({'userName' : usrName, 'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30) }, tokenKey)
        return token

    def authenticate_token(self,auth_token):
        try:
            payload = jwt.decode(auth_token, tokenKey)
            if payload:
                return True
        except :
            return "Invalid token"
