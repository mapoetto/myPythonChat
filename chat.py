import socket
import msvcrt
import time
import sys

def being_client():

	listCharacters = []

	host = input("Insert host (blank for default localhost): ")
	port = int(input("Insert port: "))
	if len(host) == 0:
		host = "localhost"


	print("ok here we go, i will try to connect to this server: " + host +  " port: " + str(port))

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		print("YEAH! we got the connection!!")
		while True:

			if msvcrt.kbhit():
				question = input("Write a question: ")
				s.sendall(bytes(question, 'utf-8'))
			else:
				s.sendall(bytes("NOP", 'utf-8'))

			data = s.recv(1024)
			answ = str(repr(data))
			if answ == "b'NOP'":
				pass #NO OPERATION
			else:
				print("Answer: ", answ[1:]) #elimina la b iniziale messa da python, ovviamente ci sarebbero 3mila controlli da fare prima di questa operazione



def being_server():

	listCharacters = []

	port = int(input("Insert port for hosting: "))

	print("ok i've setted server on port: " + str(port))
	print("Feeling lonley.... waiting for friend to join :)")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
		soc.bind(("localhost",port))
		soc.listen()
		conn, addr = soc.accept()
		with conn:
			print('YEAH! we got the connection with my friend: ', addr)
			while True:
				if msvcrt.kbhit():
					question = input("Write a question: ")
					conn.sendall(bytes(question, 'utf-8'))
				else:
					conn.sendall(bytes("NOP", 'utf-8'))

				data = conn.recv(1024)
				answ = str(repr(data))
				if answ == "b'NOP'":
					pass #NO OPERATION
				else:
					print("Answer: ", answ[1:]) #elimina la b iniziale messa da python, ovviamente ci sarebbero 3mila controlli da fare prima di questa operazione


print("Welcome on my TCP based chat")
print("This chat is NON-BLOCKING... or at least it seems to be :P ")
role = int(input("Do u wanna be a server or a client? Reply: 1 for server, 2 for client: "))

if role == 1:
	being_server()
elif role == 2:
	being_client()
else:
	print("unknown reply")
