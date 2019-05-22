import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import os

import socket, json, os.path

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')

class Peer4(Resource):
    def post(self):

        # texto enviado pelo cliente para contagem
        args = parser.parse_args()

        print("Texto enviado pelo cliente: " + args['text'])

        end = 'Arquivos'
        dire = os.listdir(end)
        dire.insert(0,'127.0.0.1')
        string = str(dire)
        b = "[],''"
        for i in range(0,len(b)):
            string =string.replace(b[i],"")

        return jsonify({
                    "count":  string,
        })

api.add_resource(Peer4, '/peer4', methods=['GET','POST'])

if __name__ == '__main__':
    app.run(threaded = True, debug = True, host='127.0.0.1', port = 5003)
