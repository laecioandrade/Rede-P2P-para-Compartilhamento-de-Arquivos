import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread

import socket, json, os.path

def ts(str):
	s.send(str.encode()) 
	data = ''
	data = s.recv(1024).decode()
	dados = data
	return dados

#Cenexão com peer1
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 6001
print(host)
print(port)
serversocket.bind((host, port))

serversocket.listen(5)
print('Iniciando a escuta!')
while 1:
	(clientsocket, address) = serversocket.accept()
	print ("Conexão ok!")
	arq = clientsocket.recv(1024).decode()
	print(arq)

	r = 'Tratando dados...'
	clientsocket.send(r.encode())

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1',6003))
	dados1=ts(arq)
	print(dados1)
	s.close ()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1',6004))
	dados2 = ts(arq)
	print(dados2)
	s.close ()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1',6005))
	dados3 = ts(arq)
	print(dados3)
	s.close ()

	qtd = 0;
	hash_tam = []
	lista = []*1
	hash_adc = []
	if dados1 != 'Erro':
		dados1 = dados1.split()
		for i in dados1:
			if i == arq:
				qtd +=1
				lista.append(dados1[0])
				lista.append(dados1[1])
				hash_adc.append(dados1[2])
				hash_tam.append(dados1[3])
				break;
	if dados2 != 'Erro':
		dados2 = dados2.split()
		for i in dados2:
			if i == arq:
				qtd +=1
				lista.append(dados2[0])
				lista.append(dados2[1])
				hash_adc.append(dados2[2])
				hash_tam.append(dados2[3])
				break;
	if dados3 != 'Erro':
		dados3 = dados3.split()
		for i in dados3:
			if i == arq:
				qtd +=1
				lista.append(dados3[0])
				lista.append(dados3[1])
				hash_adc.append(dados3[2])
				hash_tam.append(dados3[3])
				break;

	if qtd!=0:
		if qtd == 1:
			tamanho = int(hash_tam[0])
			lista.insert(0,str(qtd))
			lista.append(str(tamanho))
			lista.append(hash_adc[0])
			lista.append(arq)
			print(lista)
		if qtd == 2:
			tamanho = int(hash_tam[0])
			if (tamanho % 2 == 0):
				tam1 = int(tamanho/2)
				tam1 = int(tam1+tam1/2)
			else:
				tam1 = int(tamanho/2)
				tam1 = int(tam1+tam1/2)
			#print(tam2)
			tam2 = tamanho-tam1
			#print(tam3)
			#print(int(tam1)+int(tam2)+int(tam3))
			lista.insert(0,str(qtd))
			lista.append(str(tam1))
			lista.append(str(tam2))
			lista.append(hash_adc[0])
			lista.append(arq)
			print(lista)
		if qtd == 3:
			tamanho = int(hash_tam[0])
			if (tamanho % 2 == 0):
				tam1 = int(tamanho/2)
			else:
				tam1 = int(tamanho/2)
			#print(tam1)
			tam2 = tamanho-tam1
			if (tam2 % 2 == 0):
				aux = int(tam2/2)
				tam2 = int(aux) + int(aux/2)
			else:
				aux = int(tam2/2)
				tam2 = int(aux) + int(aux/2)
			#print(tam2)
			tam3 = tamanho-tam1-tam2
			#print(tam3)
			#print(int(tam1)+int(tam2)+int(tam3))
			lista.insert(0,str(qtd))
			lista.append(str(tam1))
			lista.append(str(tam2))
			lista.append(str(tam3))
			lista.append(hash_adc[0])
			lista.append(arq)
			print(lista)
		

	arquivo = open('torrent.txt', 'w')
	for i in lista:
		arquivo.write(i+' ')
	arquivo.close()

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
	print("Conectando com scliente...")
	s.connect((host,6002))
	 
	print("Abrindo arquivo torrent...")
	arq=open('torrent.txt','rb')
	 
	print("Enviando arquivo...")

	for i in arq:
		s.send(i)

	print("Enviado com sucesso...")
	arq.close()
	s.close()

	