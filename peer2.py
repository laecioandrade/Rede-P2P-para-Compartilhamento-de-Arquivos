import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import os

import socket, json, os.path

HOST = '127.0.0.1' 
PORT = '4001'

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')

class Peer2(Resource):
    def post(self):

        # texto enviado pelo cliente para contagem
        args = parser.parse_args()

        print("Texto enviado pelo cliente: " + args['text'])

        end = 'Arquivos'
        dire = os.listdir(end)
        dire.insert(0,HOST)
        dire.insert(0,PORT)
        string = str(dire)
        b = "[],''"
        for i in range(0,len(b)):
            string =string.replace(b[i],"")
        #dire.insert(0,'192.168.0.116')
        #string = str(dire)
        b = "[],''"
        for i in range(0,len(b)):
            string =string.replace(b[i],"")

        return jsonify({
                    "count":  string,
        })

"""s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("conectando com servidor...")
s.connect((HOST,PORT))

print("abrindo arquivo...")
end = 'Arquivos'
arq=open(end+'/ola.pdf','rb')

print("enviado  arquivo")
for i in arq:
    #print i
    s.send(i)"""



api.add_resource(Peer2, '/peer2', methods=['GET','POST'])

if __name__ == '__main__':
    app.run(threaded = True, debug = True, host='127.0.0.1', port = 4001)
