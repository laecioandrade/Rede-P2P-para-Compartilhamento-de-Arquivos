import hashlib
#import md5
  
# initializing string 
#print("abrindo arquivo...")
#arq = open('Treino.pdf','rb')

#print("abrindo arquivo2...")
#arq2 = open('saida.pdf','rb')

def file_as_bytes(file):
	with file:
		return file.read()


# encoding GeeksforGeeks using encode() 
# then sending to md5() 
result  = hashlib.md5(file_as_bytes(open('Treino.pdf', 'rb'))).hexdigest()
result2  = hashlib.md5(file_as_bytes(open('saida.pdf', 'rb'))).hexdigest()
print(result)
print('\n\n\n\n\n')
print(result2) 
# printing the equivalent hexadecimal value. 
if result == result2:
	print('Hash bateu, arquivos iguais')
else:
	print('Arquivos diferentes né bichão')
#print(result.hexdigest()) 
