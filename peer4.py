import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import hashlib

import socket, json, os.path

def file_as_bytes(file):
    with file:
        return file.read()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 6005
print (host)
print (port)
serversocket.bind((host, port))

serversocket.listen(5)
print('server started and listening')

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,7005))
s.listen(5)
while 1:
    (clientsocket, address) = serversocket.accept()
    print ("connection found!")
    data = clientsocket.recv(1024).decode()
    print(data)
    end = 'Arquivos'
    dire = os.listdir(end)
    for i in dire:
        if i == data:
            hash_data = hashlib.md5(file_as_bytes(open(end+'/'+data, 'rb'))).hexdigest()
            arq=open(end+'/'+data,'rb')
 
            #print("enviado  arquivo")
            tam=0
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
    dire.insert(0,7005)

    #print(dire)
    string = str(dire)
    b = "[],''"
    for i in range(0,len(b)):
        string =string.replace(b[i],"")

    clientsocket.send(string.encode())
    #dire.insert(0,'192.168.0.116')
    #string = str(dire)

    print("conexão encontrada!")
    conn, addr = s.accept()
    arq2= conn.recv(1024).decode() 
    print(arq2)
    arq2 = arq2.split()
    print(arq2)

    '''s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("conectando com servidor...")
    s.connect((HOST,PORT))
    print("abrindo arquivo...")
    arq=open(end+'/'arq2[0],'rb')
    print("enviado  arquivo")
    cont=0
    tam = int(arq2[1])
    for i in arq:
        cont+=1
        if cont<tam:
            #print i
            s.send(i)
    #print(cont)
    print("saindo...")
    arq.close()
    s.close()'''