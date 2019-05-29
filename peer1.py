import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import hashlib
import socket, json, os.path

def ts(str):
	s.send(str.encode()) 

def file_as_bytes(file):
	with file:
		return file.read()

def check_ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus

HOST = "127.0.0.1"
PORT = 6001
while True:
	x = input("\n\n1-Procurar arquivo\n2-Baixar PDF\n3-Sair\n")
	if x == '1':
		#Enviando nome do arquivo para tracker
		y = input("\n\nQual o nome do arquivo?\n")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		ts(y)
		s.close ()

		print("recebendo o arquivo...")
		arq = open('torrent/torrent.txt','wb')
		#Recebendo arquivo com os dados
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Escutando a porta...")
		s.bind((HOST,6002))
		s.listen(2)
	 
		print("Aceitando a conexao...")
		conn,addr= s.accept()
		res = [] 
		#Escrevendo arquivo em um arquivo local
		while 1:
			dados=conn.recv(1024)
			if not dados:
				break
			arq.write(dados)    
	 
		print(".torrent recebido...")
		conn.close()
		arq.close()
		s.close()
		#Lendo arquivo local para pegar dados
		res = []
		arq = open('torrent/torrent.txt','r')
		texto = arq.readlines()
		for linha in texto :
		    res = linha
		arq.close()
		#Criando lista de dados
		res = res.split()
		print(res)

		#PSeparando dados da lista
		tam_blocks = []
		hosts = []
		ports = []
		qtd_peers = res[0]
		fim1 = int(qtd_peers)*2
		fim2 = fim1 + int(qtd_peers) + 1
		for i in range(1,fim1,2):
			ports.append(res[i])
			hosts.append(res[i+1])
		for i in range((fim1+1),fim2,1):
			tam_blocks.append(res[i])
		cod_hash=res[fim2]
		nome_arq=res[fim2+1]
		
		#Mostrando dados
		print(cod_hash)
		print(nome_arq)
		print(tam_blocks)
		print(hosts)
		print(ports)

		tamanho = int(tam_blocks[0])+int(tam_blocks[1])+int(tam_blocks[2])
		tamanho = str(tamanho)



		print(".torrent foi um sucesso!")

	elif x == '2':
		print('Porta de envio')
		porta_env = '6009'
		print('Vamos baixar seu aquivo jaja...')
		
		'''start = time.time()
		pingstatus = check_ping('192.168.0.111')
		tempo = time.time()-start
		print(tempo)
		print(pingstatus)'''
		#Pegando tempo para verificação de distância
		'''times = []
		for i in range(len(hosts)):
			#print(hosts[i])
			#print(ports[i])
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			start = time.time()
			sock.connect_ex((str(hosts[i]), int(ports[i])))
			times.append((time.time()-start))
			sock.close()
		print(times)'''



		#Verificar tempos
		'''if times[0]<=times[1] and times[1]<=times[2]:
			print("1,2,3")
		elif times[1]<=times[0] and times[0]<=times[2]:
			print("2,1,3")
		elif times[0]<=times[1] and times[1]>=times[2]:
			print("1,3,2")
		elif times[0]>=times[1] and times[1]<=times[2]:
			print("2,1,3")
		else:
			print("3,2,1")'''

		pedido = []

		pedido.append(nome_arq)
		pedido.append(tam_blocks[0])
		pedido.append(porta_env)
		pedido.append(HOST)
		pedido.append(tamanho)

		pedido = ' '.join(pedido)
		#print(str(hosts[0]))
		#print(int(ports[0]))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((str(hosts[0]),int(ports[0])))
		ts(pedido)
		#time.sleep(5) 
		s.close()

		del pedido

		pedido = []

		pedido.append(nome_arq)
		pedido.append(tam_blocks[1])
		pedido.append(porta_env)
		pedido.append(HOST)
		pedido.append(tamanho)

		pedido = ' '.join(pedido)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((str(hosts[1]),int(ports[1])))
		ts(pedido)
		#time.sleep(5) 
		s.close()

		del pedido

		pedido = []

		pedido.append(nome_arq)
		pedido.append(tam_blocks[2])
		pedido.append(porta_env)
		pedido.append(HOST)
		pedido.append(tamanho)

		pedido = ' '.join(pedido)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((str(hosts[2]),int(ports[2])))
		ts(pedido)
		#time.sleep(5) 
		s.close()

		print("recebendo o arquivo...")
		saida = open('Download/saida.pdf','wb')

		i=0
		print(len(hosts))
		while i < len(hosts):
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print("Escutando a porta...")
			s.bind(('127.0.0.1',int(porta_env)))
			s.listen(2)
		 
			print("Aceitando a conexao...")
			conn,addr= s.accept()
			 	 
			while 1:
				dados=conn.recv(1024)
				if not dados:
					break
				saida.write(dados)    
			 
			print("saindo...")
			conn.close()
			i+=1
		saida.close()

		result  = hashlib.md5(file_as_bytes(open('Download/saida.pdf', 'rb'))).hexdigest()
		if result == cod_hash:
			print('Hash bateu, arquivos iguais')
		else:
			print('Arquivos diferentes né bichão')


	elif x == '3':
		print("Saindo...")
		break
	else:
		print("Opção invalida!")