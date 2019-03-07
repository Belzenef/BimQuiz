#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:17:49 2019

@author: ejacquemet
"""

from socket import *
#import select
from time import time, ctime
import sys
#import signal

# Pour éviter l'erreur récurente "port already in use" lors des arrets 
# repetés de vos codes serveurs, utiliser l'option socket suivante: 

comSocket = socket(AF_INET, SOCK_STREAM)
comSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

class Client:
	def __init__(self,ch):
		# Attributs
		self.name = ch
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.connect(('127.0.0.1',8000))
		self.sock.sendall(name.encode('ascii'))
		response = sock.recv(1024)
		connected=True
		if not response : 
			print("Server has been deconnected")
			connected=False
		else : 
			response=response.decode('ascii')
			print("Welcome, %s ! :) \nTo start a new Quizz enter 'start'" % response)
			print("To wait for firends, enter 'wait' ")
			print("To quit server, enter 'quit' ")
		while connected :
			line=input(">")
			line+="\x00"
			if line == "quit\x00" : 
				print("Ending connection")
				sock.sendall(line.encode('ascii'))
				connected=False
			elif line == "wait\x00" :
				response = sock.recv(1024)
				if not response : 
					print("Server has been deconnected")
					connected=False
				else : 
					response=response.decode('ascii')
					print(response)
			elif line == "start\x00" :
				line=line.encode('ascii')
				sock.sendall(line)
				response = sock.recv(1024)
				if not response : 
					print("Server has been deconnected")
					connected=False
				else : 
					response=response.decode('ascii')
					print(response)
 			else :
 				print("Sorry, I didn't get what you said ?")
				
		sock.close()

if __name__ == "__main__":
	try:
		if len(sys.argv)>=2 :
			ch=sys.argv[1]
		else : 
			ch=input('Choose nickname > ')
		while ch=="" :
			print("Sorry this nickname is not available !")
			ch=input('Choose nickname > ')
		Client(ch)
	except KeyboardInterrupt :
		print("Quiting server")
	except:
		print("Unexpected exception ... Sorry :/")
	finally :
		print('Thanks for playing ! ^_^ ')
