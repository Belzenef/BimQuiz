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
        self.connected=False
        print("Waiting connection...")
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('127.0.0.1',8000))
        self.sock.sendall(self.name.encode('ascii'))
        response = self.sock.recv(1024).decode('ascii')
        print("Welcome, %s ! :) \nTo start a new Quizz enter 'start'" % response)
        print("To wait for friends, enter 'wait' ")
        print("To quit server, enter 'quit' ")
        self.connected=True
        inp='1'
        try :
            while self.connected :
                if inp=='1' :
                    line=input(">")
                    line+="\x00"
                    if line == "quit\x00" : 
                        print("Ending connection")
                        self.sock.sendall(line.encode('ascii'))
                        self.connected=False
                    elif line == "wait\x00" :
                        inp=self.lire(self.sock)
                    elif line == "start\x00" :
                        line=line.encode('ascii')
                        self.sock.sendall(line)
                        inp=self.lire(self.sock)
                    else :
                        line=line.encode('ascii')
                        self.sock.sendall(line)
                        inp=self.lire(self.sock)
                else : 
                    inp=self.lire(self.sock)
        except KeyboardInterrupt :
            print("Ending connection")
            line = "quit\x00"
            self.sock.sendall(line.encode('ascii'))
        finally :
            self.sock.close()

    def lire(self,sock):
        res = '0' # entier (0 si pas de réponse attendue, 1 si réponse attendue, 3 si test connexion)
        response = sock.recv(1024).decode('ascii')
        if not response : 
            print("Server has been deconnected")
            self.connected=False
        else :
            res=response[-1]
            if res=='3' :
                sock.send(response[:-1].encode('ascii'))
                res='0'
            else :
                print(response[:-1])
        return res

if __name__ == "__main__":
    #try:
        if len(sys.argv)>=2 :
                ch=sys.argv[1]
        else : 
            ch=input('Choose nickname > ')
        while ch=="" :
            print("Sorry this nickname is not available !")
            ch=input('Choose nickname > ')
        Client(ch)
    #except KeyboardInterrupt :
        #print("Quiting server")
    #except:
        #print("Unexpected exception ... Sorry :/")
    #finally :
        #print('Thanks for playing ! ^_^ ')
