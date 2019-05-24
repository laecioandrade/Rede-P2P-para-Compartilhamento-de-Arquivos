import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import os

import socket, json, os.path

HOST = '127.0.0.1' 
PORT = '4002'

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')

class Peer3(Resource):
    def post(self):

        # texto enviado pelo cliente para contagem
        args = parser.parse_args()

        print("Texto enviado pelo cliente: " + args['text'])

        end = 'Arq'
        dire = os.listdir(end)
        dire.insert(0,HOST)
        dire.insert(0,PORT)
        string = str(dire)
        b = "[],''"
        for i in range(0,len(b)):
            string =string.replace(b[i],"")

        return jsonify({
                    "count":  string,
        })



api.add_resource(Peer3, '/peer3', methods=['GET','POST'])

if __name__ == '__main__':
    app.run(threaded = True, debug = True, host='127.0.0.1', port = 4002)
