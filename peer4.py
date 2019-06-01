import requests, string, asyncio, time
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from threading import Thread
import hashlib

import socket, json, os.path

def file_as_bytes(file):
    with file:
        return file.read()

def hashFor(data):
    # Prepare the project id hash
    hashId = hashlib.md5()

    hashId.update(repr(data).encode('utf-8'))

    return hashId.hexdigest()
#Conexão com Tracker
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 6005
print (host)
print (port)
serversocket.bind((host, port))
serversocket.listen(5)
print('Iniciando a escuta!')
#Conexão com o peer1
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,7005))
s.listen(5)

while 1:
    (clientsocket, address) = serversocket.accept()
    print ("Conexão ok!")
    data = clientsocket.recv(1024).decode()
    print("O arquivo solicitado é: ",data)
    end = 'Arquivo_peer4'
    dire = os.listdir(end)
    tam=0

    verifica_arquivo=0
    #Verificando arquivo esta no diretorio
    for i in dire:
        if i == data:
            verifica_arquivo=1
            #Pegando hash do arquivo
            #aux_arq_hash =  open(end+'/'+data,'rb')
            #hash_data  = hashFor(aux_arq_hash)
            #aux_arq_hash.close()
            hash_data = hashlib.md5(file_as_bytes(open(end+'/'+data, 'rb'))).hexdigest()
            arq=open(end+'/'+data,'rb')
            
            for i in arq:
                tam+=1

            arq.close()

    #O processo a seguir só ira ocorrer se o peer possuir o arquivo
    if verifica_arquivo==1:
        #Adicionado tamanho total do arquivo
        dire.insert(0,tam)
        #Adicinando codigo hash do arquivo
        dire.insert(0,hash_data)
        #Adicinando IP do peer
        dire.insert(0,host)
        #Adicionando PORTA que ira ser utilizada para pediar arquivo
        dire.insert(0,7005)

        string = str(dire)
        b = "[],''"
        for i in range(0,len(b)):
            string =string.replace(b[i],"")

        clientsocket.send(string.encode())

        #Recebendo pedido
        print("Conexão de pedido ok!")
        conn, addr = s.accept()
        arq2= conn.recv(1024).decode() 
        print(arq2)
        arq2 = arq2.split()
        print(arq2)
    
        if int(arq2[5]) == 1:
            tam_env = 0
            tam_fim = int(arq2[4])+1
            time.sleep(2)
        if int(arq2[5]) == 2:
            if int(arq2[6]) == 0:
                tam_env = 0
                tam_fim  = int(arq2[1])
                time.sleep(2)
            else:
                tam_env = int(arq2[1])
                tam_fim = int(arq2[4])+1
                time.sleep(4)
        if int(arq2[5]) == 3:
            if int(arq2[6]) == 0:
                tam_env =0
                tam_fim = int(arq2[1])
                time.sleep(2)
            elif int(arq2[6]) == 1:
                tam_env = (int(arq2[4])-int(arq2[1]))-(int(arq2[1])/3)
                tam_fim = tam_env+int(arq2[1])
                time.sleep(4)
            else:
                tam_env = int(arq2[4])-int(arq2[1])
                tam_fim = int(arq2[4])+1
                time.sleep(6)
        

        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Conectando com cliente...")
        sock.connect((arq2[3],int(arq2[2])))
        print(arq2[0])
        print("abrindo arquivo...")
        arq_aux=open(end+'/'+arq2[0],'r+b')
        print("enviando  arquivo")
        cont=1

        tam_env = int(tam_env)
        tam_fim = int(tam_fim)
        print("Inicio = ",tam_env)
        print("Fim =", tam_fim)
        for i in arq_aux:
            if tam_env==cont and tam_env<tam_fim:
                sock.send(i)
                tam_env+=1
            cont+=1
        print(tam_env)
        print(cont)
        print("Enviado com sucesso!...")
        arq_aux.close()
        sock.close()
    else:
        string='Erro'
        clientsocket.send(string.encode())