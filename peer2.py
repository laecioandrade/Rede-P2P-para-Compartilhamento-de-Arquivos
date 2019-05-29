import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import hashlib

import socket, json, os.path

def file_as_bytes(file):
    with file:
        return file.read()


host = '127.0.0.1'
port = 6003
print (host)
print (port)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)

print('server started and listening')

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,7003))
s.listen(5)


while 1:

    (clientsocket, address) = serversocket.accept()
    print ("connection found!")
    data = clientsocket.recv(1024).decode()
    print(data)
    end = 'Arquivo_peer2'
    dire = os.listdir(end)
    tam=0
    for i in dire:
        if i == data:
            hash_data = hashlib.md5(file_as_bytes(open(end+'/'+data, 'rb'))).hexdigest()
            arq=open(end+'/'+data,'rb')
 
            #print("enviado  arquivo")
            for i in arq:
                tam+=1
                    #print i
                #s.send(i)
            #print(cont)
            #print("saindo...")
            arq.close()
            #s.close()
    dire.insert(0,tam)
    dire.insert(0,hash_data)
    dire.insert(0,host)
    dire.insert(0,7003)

    string = str(dire)
    b = "[],''"
    for i in range(0,len(b)):
        string =string.replace(b[i],"")

    clientsocket.send(string.encode())


    print("conexão encontrada!")
    conn, addr = s.accept()
    arq2= conn.recv(1024).decode() 
    print(arq2)
    arq2 = arq2.split()
    print(arq2)


    time.sleep(2)
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     
    print("conectando com servidor...")
    sock.connect((arq2[3],int(arq2[2])))
    print(arq2[0])
    print("abrindo arquivo...")
    arq_aux=open(end+'/'+arq2[0],'r+b')
     
    print("enviando  arquivo")
    cont=1
    z=0

    print("Inicio = ",cont)
    print("Fim =", int(arq2[1]))
    for i in arq_aux:
        if (cont<int(arq2[1])):
            #print i
            sock.send(i)
        cont+=1
        z+=1
    print(z)
     
    print("saindo...")
    arq_aux.close()
    #arq.close()
    sock.close()