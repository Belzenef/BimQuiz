import multiprocessing
import socket
import select
from time import time, ctime
import sys
import signal

 
class Serveur:
	def __init__(self):
		stopBoolServ = True
		# Initialisation de la classe """
		self.clients ={}
		self.TAILLE_BLOC=1024 # la taille des blocs 
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(("127.0.0.1",8888))
		sock.listen(5)
		print("Listening")
		while True:
			con, addr = sock.accept()
			print"Quelqu'un vient de se connecter!"
			pseudo = sockClient.recv(self.TAILLE_BLOC)
			self.clients[pseudo] = con
			print "soucis"
			process = multiprocessing.Process(target=handle_com, args=(con, addr))
			print "soucis 2"
			process.daemon = True
			process.start()
			print "soucis 3"
			#print"process {0}".format(process)

		
	def handle_com(sockClient, self):
		#print "process identity {0}".format(self,)
		try:
			#print "connection information {0} at {1}".format(sockClient, self)
			while True:
				data = sockClient.recv(self.TAILLE_BLOC)
				if data == "quit":
					print "Socket closed by client ?"
					break
				print"Message recu: {0}".format(data)
				sockClient.sendall(data)
				print"Envoi du message"
		except:
			print"Problem in request ?"
		finally:
			print"finally : Closed socket"
			sockClient.close()
 
 
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
	
