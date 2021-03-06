import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import hashlib
import socket, json, os.path
import socket, select, string, sys
from PyQt5.QtWidgets import *
from _thread import *
import time
import os
import subprocess
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QBasicTimer

class ChatWindow(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()

		print('Bem-Vindo!')

    #Iniciando a UI    
	def initUI(self):

		self.messageField = QLineEdit()
		self.messageList = QListWidget()
		self.nickLabel = QLabel("\n\tSeja Bem-Vindo!\n\nQual o nome do arquivo que você deseja?", self)

		self.nickField = QLineEdit()
		self.connectButton = QPushButton("Vizualizar Arquivos")
		self.nickButton = QPushButton("Baixar")
		self.nickButton.setAutoDefault(True)

		self.nickField.returnPressed.connect(self.nickButton.click)

		self.nickField.returnPressed.connect(self.connectButton.click)

		self.nickButton.clicked.connect(self.downloadButtonClicked)

		self.connectButton.clicked.connect(self.connectButtonClicked)

		self.progress = QProgressBar(self)
		self.progress.setGeometry(0, 0, 300, 25)
		self.progress.setMaximum(100)

		connectLayout = QWidget()
		vbox1 = QVBoxLayout()

		vbox1.addWidget(self.nickLabel)
		vbox1.addWidget(self.nickField)
		vbox1.addWidget(self.nickButton)

		vbox1.addWidget(self.progress)

		vbox1.addWidget(self.connectButton)
		vbox1.addStretch(1)
		connectLayout.setLayout(vbox1)
		connectLayout.setFixedWidth(300)
		vbox3 = QHBoxLayout()
		vbox3.addWidget(connectLayout)



		hbox2 = QHBoxLayout()
		hbox2.addLayout(vbox3)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox2)

		self.setLayout(vbox)

		self.resize(720, 480)
		self.center()

		self.setWindowTitle('sdTorrent')    
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

    #Botão para baixar arquivos
	def downloadButtonClicked(self):

		string = self.nickField.text()
		self.aguarde()
		res_env = self.envio(str(string))
		self.nickname = self.nickField.text()
		print(string)
		#if res == 1:
		#	self.conexao_res()
		if res_env == 'ok':
			count = 0
			TIME_LIMIT = 100
			while count < TIME_LIMIT:
				count += 1
				time.sleep(0.09)
				self.progress.setValue(count)
			self.concluido()
		elif res_env == 'erro_c':
			self.conexao_erro()
		else:
			self.conexao_res()
		self.nickField.clear()        
		return

	#Butão para ir para diretorio de arquivos
	def connectButtonClicked(self):

		subprocess.check_call(["xdg-open", 'Download'])
		return

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Sair',
			"Deseja realmente sair?", QMessageBox.Yes | 
			QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def  aguarde(self):
		QMessageBox.about(self, "Aviso" , "Aguarde enquanto preparamos seu arquivo!" )

	def conexao_res(self):
		QMessageBox.about(self, "Aviso" , "Arquivo não encontrado!" )

	def conexao_erro(self):
		QMessageBox.about(self, "Aviso" , "Servidor indisponivel!" )

	def  concluido(self):
		QMessageBox.about(self, "Aviso" , "Seu download foi concluido!" )

	def set_settings(self):
		self.resize(350,200)

	#def ts(self, str):
		

	def file_as_bytes(self, file):
		with file:
			return file.read()

	def check_ping(self,hostname):
	    os.system("ping -c 1 " + hostname)

	def hashFor(self, data):
	    # Prepare the project id hash
	    hashId = hashlib.md5()
	    hashId.update(repr(data).encode('utf-8'))
	    return hashId.hexdigest()

	def envio(self, nome_arq):
		HOST = "192.168.0.111"
		PORT = 6001
		#Enviando nome do arquivo para tracker
		exception = 0
		resultado_res =0
		print(nome_arq)
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#IP do trakeR
			s.connect(('192.168.0.102',PORT))
			s.send(nome_arq.encode())
			s.close ()
		except:
			exception=1
			resultado_res=1

		if exception==0:


			print("Recebendo o arquivo .torrent...")
			arq = open('torrent/torrent.txt','wb')
			#Recebendo arquivo com os dados
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#print("Escutando a porta...")
			s.bind(('',6002))
			s.listen(2)
		 
			#print("Aceitando a conexao...")
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
			print(res)
			#print(res)
			#Criando lista de dados
			if res != []:
				res = res.split()
				#print(res)

				#Preparando dados da lista
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
				#print(cod_hash)
				#print(nome_arq)
				#print(tam_blocks)
				#print(hosts)
				#print(ports)

				tamanho=0
				for i in range(len(hosts)):
					tamanho+=int(tam_blocks[i])
				tamanho = str(tamanho)
				
				print('\n')
				print('Tamanho dos blocos')
				print(tam_blocks)
				print('Tamanho')
				print(tamanho)
				print('\n')


				print('Porta de envio')
				porta_env = '6009'
				print('Vamos baixar seu aquivo jaja...')
				time1 = 0
				time2 = 0
				time3 = 0
				if qtd_peers == 1:
					start = time.time()
					check_ping(hosts[0])
					time1 = time.time()-start
					del start
				if qtd_peers == 2:
					start = time.time()
					check_ping(hosts[0])
					time1 = time.time()-start

					start = time.time()
					check_ping(hosts[1])
					time2 = time.time()-start
					del start
				if qtd_peers == 3:
					start = time.time()
					check_ping(hosts[0])
					time1 = time.time()-start

					start = time.time()
					check_ping(hosts[1])
					time2 = time.time()-start

					start = time.time()
					check_ping(hosts[2])
					time3 = time.time()-start
					del start
					

				print(time)

				qtd_peers = len(hosts)
				#Verificar tempos
				if qtd_peers == 1:
					pedido = []

					pedido.append(nome_arq)
					pedido.append(tam_blocks[0])
					pedido.append(porta_env)
					pedido.append(HOST)
					pedido.append(tamanho)
					pedido.append(qtd_peers)
					pedido.append('0')

					pedido = ' '.join(map(str, pedido))
					#print(str(hosts[0]))
					#print(int(ports[0]))
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((str(hosts[0]),int(ports[0])))
					s.send(pedido.encode())
					#time.sleep(5) 
					s.close()

					del pedido
				if qtd_peers == 2:
					if time1 <= time2:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("1,2")
					else:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("2,1")
				if qtd_peers == 3:
					if time1<=time2 and time2<=time3:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[2])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('2')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[2]),int(ports[2])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("1,2,3")
					elif time1<=time2 and time3<=time2:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						#pedido = ' '.join(pedido)
						pedido = ' '.join(map(str, pedido))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[2])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('2')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[2]),int(ports[2])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("1,3,2")
					elif time2<=time1 and time1<=time3:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[2])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('2')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[2]),int(ports[2])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("2,1,3")
					elif time2<=time3 and time3<=time1:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[2])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('2')

						pedido = ' '.join(map(str, pedido))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[2]),int(ports[2])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("2,3,1")
					elif time3<=time1 and time1<=time2:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[2])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('2')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[2]),int(ports[2])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("3,1,2")
					else:
						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[2])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('2')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[0]),int(ports[0])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[1])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('1')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[1]),int(ports[1])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido

						pedido = []

						pedido.append(nome_arq)
						pedido.append(tam_blocks[0])
						pedido.append(porta_env)
						pedido.append(HOST)
						pedido.append(tamanho)
						pedido.append(qtd_peers)
						pedido.append('0')

						pedido = ' '.join(map(str, pedido))
						#print(str(hosts[0]))
						#print(int(ports[0]))
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((str(hosts[2]),int(ports[2])))
						s.send(pedido.encode())
						#time.sleep(5) 
						s.close()

						del pedido
						print("3,2,1")

				print("Recebendo o arquivo...")
				saida_a = open('Download/'+nome_arq,'wb')

				i=0

				s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				#print("...")
				s.bind(('',int(porta_env)))
				s.listen(2)
				print(len(hosts))
				while i < len(hosts):
					
				 
					print("...")
					conn,addr= s.accept()
					 	 
					while 1:
						dados=conn.recv(1024)
						if not dados:
							break
						saida_a.write(dados)    
					 
					print("...")
					
					i+=1
				saida_a.close()
				conn.close()
				s.close()
				print("Arquivo baixado...")

				#aux_arq_hash =  open('Download/saida.pdf','rb')
				#result  = hashFor(aux_arq_hash)
				#aux_arq_hash.close()
				result  = hashlib.md5(self.file_as_bytes(open('Download/'+nome_arq, 'rb'))).hexdigest()
				print(cod_hash)
				print(result)
				if result == cod_hash:
					print('Otimas noticias, o Hash bateu, arquivos iguais')
				else:
					print('Arquivos diferentes né bichão')
				del result
				del cod_hash
				return 'ok'
			else:
				print('Nenhum peer tem o arquivo!')
				return 'erro'
		else:
			return 'erro_c'



			#print(".torrent foi um sucesso!")

		#elif x == '2':
			
		#return resultado_res

	#def onButtonClick(self):
	#def on_button_clicked(self):
		#alert = QMessageBox()
		#alert.setText('You clicked the button!')


if __name__ == '__main__':

	app = QApplication(sys.argv)
	cw = ChatWindow()
	sys.exit(app.exec_())
