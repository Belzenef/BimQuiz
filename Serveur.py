from multiprocessing import *
from multiprocessing import Queue
from multiprocessing.sharedctypes import Value, Array
from socket import *
import select
from time import time, ctime
import sys
import signal
import traceback

comSocket = socket(AF_INET, SOCK_STREAM)
comSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


class Serveur:
	def __init__(self):
		# Initialisation de la classe """
		manager = Manager()
		self.clients = {}
		self.TAILLE_BLOC=1024 # la taille des blocs 
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind(("127.0.0.1",8000))
		self.sock.listen(5)
		self.partie_lancee=Value('i', 0)
		self.partie_en_cours=Value('i', 0)
		self.queue = Queue()
		queue.put(self.clients)
		print("Welcome to the best Quiz ever! ")
		self.run()
		
	def run(self):
		while True:
			con, addr = self.sock.accept()
			process = Process(target=self.handle_com, args=(con, addr, self.queue))
			process.daemon = True
			process.start()
			#if self.partie_lancee.value==1 :
			#	print("inside if")
				#game = multiprocessing.Process(target=self.partie, args=(self.clients))
				#game.daemon = True
				#game.start()
			#	self.partie_lancee.acquire()
			#	self.partie_lancee.value=0
			#	self.partie_lancee.release()
			#	self.partie_en_cours.acquire()
			#	self.partie_en_cours.value=1
			#	self.partie_en_cours.release()
			#	self.partie(self.clients)
		self.sock.close()

		
	def handle_com(self, sockClient, addr, queue):
		connected = True
		try:
			pseudo = sockClient.recv(self.TAILLE_BLOC)
			pseudo=pseudo.decode("ascii")
			queue.get()[sockClient]=pseudo
			print("%s joined server" % pseudo)
			response=pseudo.encode("ascii")
			sockClient.sendall(response)
			while connected:
				data = sockClient.recv(self.TAILLE_BLOC)
				data=data.decode('ascii')
				if data ==  "quit\x00":
					print("%s has left server :'(" %pseudo)
					connected=False
				elif data == "start\x00":
					if self.partie_en_cours.value==0 :
						print("Starting game ...")
						response="You started a new game !\n"
						response=response.encode("ascii")
						sockClient.sendall(response)
						self.partie_en_cours.acquire()
						self.partie_en_cours.value=1
						self.partie_en_cours.release()
						#process = multiprocessing.Process(target=self.partie, args=(self.clients))
						#process.daemon = True
						#process.start()
						self.partie(queue.get())
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
		print("Connected players : ")
		print(joueurs)
		#for sock in joueurs.keys():
		#	print(joueurs[sock])
		#	response="Welcome to the party"
		#	response=response.encode("ascii")
		#	sock.sendall(response)
 
if __name__ == "__main__":
		try:
			Serveur()
		except:
			print("Unexpected exception")
		finally:
			print("Shutting down")
			for process in active_children():
				print("Shutting down process ", process)
				process.terminate()
				process.join()
			print("END")
	
