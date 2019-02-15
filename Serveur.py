import multiprocessing
from socket import *
import select
from time import time, ctime
import sys
import signal
import traceback

comSocket = socket(AF_INET, SOCK_STREAM)
comSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
partie_en_cours=False

class Serveur:
	def __init__(self):
		# Initialisation de la classe """
		global partie_en_cours
		partie_en_cours=False
		self.clients ={}
		self.joueurs={}
		self.TAILLE_BLOC=1024 # la taille des blocs 
		sock = socket(AF_INET, SOCK_STREAM)
		sock.bind(("127.0.0.1",8888))
		sock.listen(5)
		print("Welcome to the best Quiz ever!")
		while True:
			con, addr = sock.accept()
			process = multiprocessing.Process(target=self.handle_com, args=(con, addr))
			process.daemon = True
			process.start()

		
	def handle_com(self, sockClient, addr):
		global partie_en_cours
		connected = True
		try:
			pseudo = sockClient.recv(self.TAILLE_BLOC)
			pseudo=pseudo.decode("ascii")
			self.clients[sockClient] = pseudo
			print("%s joined server" %self.clients.get(sockClient))
			response=self.clients.get(sockClient).encode("ascii")
			sockClient.sendall(response)
			while connected:
				data = sockClient.recv(self.TAILLE_BLOC)
				data=data.decode('ascii')
				if data ==  "quit\x00":
					print("%s has left server :'(" %self.clients[sockClient])
					connected=False
				elif data == "start\x00":
					print("hey")
					if not partie_en_cours :
						print("inside if")
						partie_en_cours=True
						process = multiprocessing.Process(target=self.partie, args=(self.clients))
						process.daemon = True
						process.start()
						#self.partie(self.clients)
					else :
						ch="Game already started :/"
						sockClient.sendall(ch.encode("ascii"))
				else :
					data+="\x00"
					data=data.encode("ascii")
					sockClient.sendall(data)
		except:
			print("Problem in request ?")
		finally:
			sockClient.close()


	def partie(self, joueurs):
		print("inside function")
		for sock in joueurs.keys():
			print(sock)
			sock.sendall("Welcome to the party!")
 
if __name__ == "__main__":
		try:
			Serveur()
		except:
			print("Unexpected exception")
		finally:
			print("Shutting down")
			for process in multiprocessing.active_children():
				print("Shutting down process ", process)
				process.terminate()
				process.join()
			print("END")
	
