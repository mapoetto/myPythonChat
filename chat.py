import socket
import sys
import os
import cryptography
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes

#initialization vector costante
iv = bytes.fromhex("4340ca2385ec3dc5d60035678cf38375")

def being_client():

	shouldIask = False

	host = input("Insert host (blank for default localhost): ")
	port = int(input("Insert port: "))
	if len(host) == 0:
		host = "127.0.0.1"


	print("ok here we go, i will try to connect to this server: " + host +  " port: " + str(port))

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		print("YEAH! we got the connection!!")
		print("We are client-side, so we will wait until to get a question")

		#formiamo la chiave per parlare con il server
		string_enc = host+"MYSALTISVERYSALTED" #creo una stringa univoca con IP ed un salt

		digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
		digest.update(bytes(string_enc, 'utf-8'))
		key_dec = digest.finalize()

		string_dec = socket.gethostbyname(socket.gethostname())+"MYSALTISVERYSALTED" #creo una stringa univoca con IP ed un salt

		digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
		digest.update(bytes(string_dec, 'utf-8'))
		key_enc = digest.finalize()
		
		print("USO QUESTA CHIAVE PER DECRYPTARE: "+str(binascii.hexlify(key_dec)))
		print("E QUESTA PER CRYPTARE: "+str(binascii.hexlify(key_enc))+" \n\n")

		backend = default_backend()

		while True:

			cipher_enc = Cipher(algorithms.AES(key_enc), modes.CBC(iv), backend=backend)
			cipher_dec = Cipher(algorithms.AES(key_dec), modes.CBC(iv), backend=backend)
			encryptor = cipher_enc.encryptor()
			decryptor = cipher_dec.decryptor()
			padder = padding.PKCS7(128).padder()
			unpadder = padding.PKCS7(128).unpadder()

			if shouldIask:
				question = input("Write a question: ")
				padded_data  = padder.update(bytes(question, 'utf-8')) + padder.finalize()
				message_encrypt = encryptor.update(padded_data) + encryptor.finalize()
				s.sendall(message_encrypt)
				shouldIask = False
			else:
				data = s.recv(1024)
				message_decrypt = decryptor.update(data) + decryptor.finalize()
				plain_unpad = unpadder.update(message_decrypt) + unpadder.finalize()
				answ = str(repr(plain_unpad))
				print("Answer: ", answ[1:]) #elimina la b iniziale messa da python, ovviamente ci sarebbero 3mila controlli da fare prima di questa operazione
				shouldIask = True



def being_server():

	shouldIask = True

	port = int(input("Insert port for hosting: "))

	print("ok i've setted server on port: " + str(port))
	print("Feeling lonley.... waiting for friend to join :)")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
		soc.bind(("localhost",port))
		soc.listen()
		conn, addr = soc.accept()
		with conn:
			print('YEAH! we got the connection with my friend: ', addr)
			print("debbugging: ip client: "+ addr[0] + "\n myip: " + socket.gethostbyname(socket.gethostname()))
			
			#formiamo la chiave per parlare con il client
			
			string_enc = addr[0]+"MYSALTISVERYSALTED" #creo una stringa univoca con IP ed un salt

			digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
			digest.update(bytes(string_enc, 'utf-8'))
			key_enc = digest.finalize()

			string_dec = socket.gethostbyname(socket.gethostname())+"MYSALTISVERYSALTED" #creo una stringa univoca con IP ed un salt

			digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
			digest.update(bytes(string_dec, 'utf-8'))
			key_dec = digest.finalize()
			
			print("USO QUESTA CHIAVE PER DECRYPTARE: "+str(binascii.hexlify(key_dec)))
			print("E QUESTA PER CRYPTARE: "+str(binascii.hexlify(key_enc))+" \n\n")

			backend = default_backend()

			while True:

				cipher_enc = Cipher(algorithms.AES(key_enc), modes.CBC(iv), backend=backend)
				cipher_dec = Cipher(algorithms.AES(key_dec), modes.CBC(iv), backend=backend)
				encryptor = cipher_enc.encryptor()
				decryptor = cipher_dec.decryptor()
				padder = padding.PKCS7(128).padder()
				unpadder = padding.PKCS7(128).unpadder()

				if shouldIask:
					question = input("Write a question: ")
					padded_data  = padder.update(bytes(question, 'utf-8')) + padder.finalize()
					message_encrypt = encryptor.update(padded_data) + encryptor.finalize()
					conn.sendall(message_encrypt)
					shouldIask = False
				else:
					data = conn.recv(1024)
					message_decrypt = decryptor.update(data) + decryptor.finalize()
					plain_unpad = unpadder.update(message_decrypt) + unpadder.finalize()
					answ = str(repr(plain_unpad))
					print("Answer: ", answ[1:]) #elimina la b iniziale messa da python, ovviamente ci sarebbero 3mila controlli da fare prima di questa operazione
					shouldIask = True


print("Welcome on my TCP based chat")
print("This chat is only for very educated people.... (: if you already asked a question, pls be kind and wait for the answer!!")
role = int(input("Do u wanna be a server or a client? (Server will ask first). Reply: 1 for server, 2 for client: "))

if role == 1:
	being_server()
elif role == 2:
	being_client()
else:
	print("unknown reply")

			
