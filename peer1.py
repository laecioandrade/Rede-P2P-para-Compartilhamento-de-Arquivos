import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread

import socket, json, os.path

def ts(str):
	s.send(str.encode()) 
	data = ''
	data = s.recv(1024).decode()
	res = data

HOST = "127.0.0.1"
PORT = 7001
while True:
	x = input("\n\n1-Procurar arquivo\n2-Baixar PDF\n3-Sair\n")
	if x == '1':
		y = input("\n\nQual o nome do arquivo?\n")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		ts(y)
		s.close ()

		print("recebendo o arquivo...")
		arq = open('torrent/torrent.txt','wb')

		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Escutando a porta...")
		s.bind((HOST,7002))
		s.listen(2)
	 
		print("Aceitando a conexao...")
		conn,addr= s.accept()
		res = [] 
		while 1:
			dados=conn.recv(1024)
			if not dados:
				break
			arq.write(dados)    
	 
		print(".torrent recebido...")
		conn.close()
		arq.close()
		res = []
		arq = open('torrent/torrent.txt','r')
		texto = arq.readlines()
		for linha in texto :
		    res = linha
		arq.close()

		res = res.split()
		print(res)
		print("saindo...")

	elif x == '2':
		print('calma')
		"""ips = []
		for i in range(len(x1)-1):
			ips.append(x1[i])
		print(ips)
		times = []
		for i in range(len(ips)):
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			time1 = sock.gettimeout() #2 Second Timeout
			start = time.time()
			res = sock.connect_ex(('192.168.0.116', 4001))
			times.append((time.time()-start))
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)"""
		
		#time2 = sock.gettimeout() #2 Second Timeout
		#start = time.time()
		#res = sock.connect_ex((HOST, PORT))
		#time2 = time.time()-start
		#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#time3 = sock.gettimeout() #2 Second Timeout
		#start = time.time()
		#res = sock.connect_ex(('192.168.0.144', 5003))
		#time3 = (time.time()-start)
		
		#for i in range(len(times)):
		#	print("Tempo peer %d: %f"%(i,times[i]))
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

		"""s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Escutando a porta...")
		s.bind((HOST,PORT))
		s.listen(1)
		 
		print("Aceitando a conexao...")
		conn,addr= s.accept()
		 
		print("recebendo o arquivo...")
		arq = open('File_ouputt.pdf','wb')
		print("Recebido")
		while 1:
		    dados=conn.recv(1024)
		    if not dados:
		        break
		    arq.write(dados)

		 
		print("saindo...")
		arq.close()
		conn.close()
		print("abrindo arquivo...")"""

	elif x == '3':
		print("Saindo...")
		break
	else:
		print("Opção invalida!")