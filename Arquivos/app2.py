# Servidor
 
import socket, threading
print("Servidor")
 
HOST = "localhost" 
PORT = 57000


print("recebendo o arquivo...")
arq = open('saida.pdf','wb')

i=0
while i < 2:
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Escutando a porta...")
	s.bind((HOST,PORT))
	s.listen(2)
 
	print("Aceitando a conexao...")
	conn,addr= s.accept()
	 	 
	while 1:
		dados=conn.recv(1024)
		if not dados:
			break
		arq.write(dados)    
	 
	print("saindo...")
	conn.close()
	i+=1
arq.close()

