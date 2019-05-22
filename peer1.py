import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread

import socket, json, os.path

while True:
	x = input("\n\n1-Procurar arquivo\n2-Baixar PDF\n3-Sair\n")
	if x == '1':
		y = input("\n\nQual o nome do arquivo?\n")
		retorno = requests.post("http://127.0.0.1:4000/Tracker", json={"text": y})
		if retorno.json()['count']:
			x1 = retorno.json()['count']
			print("As maquinas a seguir possuem o arquivo: ")
			print(x1)	
	elif x == '2':
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#time1 = sock.gettimeout() #2 Second Timeout
		start = time.time()
		res = sock.connect_ex(('127.0.0.1', 4001))
		time1 = (time.time()-start)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#time2 = sock.gettimeout() #2 Second Timeout
		start = time.time()
		res = sock.connect_ex(('127.0.0.1', 4002))
		time2 = time.time()-start
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#time3 = sock.gettimeout() #2 Second Timeout
		start = time.time()
		res = sock.connect_ex(('127.0.0.1', 5003))
		time3 = (time.time()-start)
		
		#print("Tempo peer 1: ",time1)
		#print("Tempo peer 2: ",time2)
		#print("Tempo peer 3: ",time3)

		#if time1<=time2 and time2<=time3:
		#	print("1,2,3")
		#elif time2<=time1 and time1<=time3:
		#	print("2,1,3")
		#elif time1<=time2 and time2>=time3:
		#	print("1,3,2")
		#elif time1>=time2 and time2<=time3:
		#	print("2,1,3")
		#else:
		#	print("3,2,1")

		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("conectando com servidor...")
		s.connect(('127.0.0.1', 4001))

		arq = open('File_ouputt1.txt','wb')
		print("Recebido")
		while 1:
			dados=conn.recv(1024)
    		if not dados:
        		break
    		arq.write(dados)
    	print("saindo...")
		arq.close()
		s.close()

		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("conectando com servidor...")
		s.connect(('127.0.0.1', 4002))

		arq = open('File_ouputt2.txt','wb')
		print("Recebido")
		while 1:
			dados=conn.recv(1024)
    		if not dados:
        		break
    		arq.write(dados)
    	print("saindo...")
		arq.close()
		s.close()

		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("conectando com servidor...")
		s.connect(('127.0.0.1', 5003))

		arq = open('File_ouputt3.txt','wb')
		print("Recebido")
		while 1:
			dados=conn.recv(1024)
    		if not dados:
        		break
    		arq.write(dados)
    	print("saindo...")
		arq.close()
		s.close()
 
print("abrindo arquivo...")

	elif x == '3':
		print("Saindo...")
		break
	else:
		print("Opção invalida!")