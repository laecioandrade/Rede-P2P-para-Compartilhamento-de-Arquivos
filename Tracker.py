import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread

import socket, json, os.path

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')

class Tracker(Resource):
	def post(self):

        # texto enviado pelo cliente para contagem
		args = parser.parse_args()
		print("Texto enviado pelo cliente: " + args['text'])
		retorno = requests.post("http://127.0.0.1:4001/peer2", json={"text": "Procurando"})
		if retorno.json()['count']:
			x1 = retorno.json()['count']
			y1 = x1.split()
			print("Retorno peer2: ",y1)
		retorno = requests.post("http://127.0.0.1:4002/peer3", json={"text": "Procurando"})
		if retorno.json()['count']:
			x2 = retorno.json()['count']
			y2 = x2.split()
			print("Retorno peer3: ",y2)
		retorno = requests.post("http://127.0.0.1:5003/peer4", json={"text": "Procurando"})
		if retorno.json()['count']:
			x3 = retorno.json()['count']
			y3 = x3.split()
			print("Retorno peer4: ",y3)

		lista = []*1

		for i in y1:
			if i == args['text']:
				lista.append('127.0.0.1')
				break;
		for i in y2:
			if i == args['text']:
				lista.append('127.0.0.1')
				break;
		for i in y3:
			if i == args['text']:
				lista.append('127.0.0.1')
				break;

		lista.append(args['text'])
		print(lista)


		return jsonify({
			"count":  lista,
		})

api.add_resource(Tracker, '/Tracker', methods=['GET','POST'])

if __name__ == '__main__':
	app.run(threaded = True, debug = True, host='127.0.0.1', port = 4000)
