# Cliente 
import socket
 
print("Clinte")
 
HOST='localhost' #coloca o host do servidor 
PORT=57000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
print("conectando com servidor...")
s.connect((HOST,PORT))
 
print("abrindo arquivo...")
arq=open('Treino.pdf','rb')
 
print("enviado  arquivo")
cont=0
for i in arq:
    cont+=1
    if cont<=100:
        #print i
        s.send(i)
print(cont)
 
print("saindo...")
arq.close()
s.close()
