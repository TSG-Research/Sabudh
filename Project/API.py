from flask import Flask, request, jsonify
app = Flask(__name__)
from clustering import *

@app.route('/wiki',methods =['GET'])
def write():
    print("HI")
    return jsonify("hi")

if __name__ == '__main__':
    app.run(debug= True)

