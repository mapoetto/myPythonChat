import socket
import sys

def being_client():

	shouldIask = False

	host = input("Insert host (blank for default localhost): ")
	port = int(input("Insert port: "))
	if len(host) == 0:
		host = "localhost"


	print("ok here we go, i will try to connect to this server: " + host +  " port: " + str(port))

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host, port))
		print("YEAH! we got the connection!!")
		print("We are client-side, so we will wait until to get a question")
		while True:
			if shouldIask:
				question = input("Write a question: ")
				s.sendall(bytes(question, 'utf-8'))
				shouldIask = False
			else:
				data = s.recv(1024)
				answ = str(repr(data))
				print("Answer: ", answ[1:]) #elimina la b iniziale messa da python, ovviamente ci sarebbero 3mila controlli da fare prima di questa operazione
				shouldIask = True



def being_server():

	shouldIask = True

	port = int(input("Insert port for hosting: "))

	print("ok i've setted server on port: " + str(port))
	print("Feeling lonley.... waiting for friend to join :)")

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
		soc.bind(("",port))
		soc.listen()
		conn, addr = soc.accept()
		with conn:
			print('YEAH! we got the connection with my friend: ', addr)
			while True:
				if shouldIask:
					question = input("Write a question: ")
					conn.sendall(bytes(question, 'utf-8'))
					shouldIask = False
				else:
					data = conn.recv(1024)
					answ = str(repr(data))
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

			
