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
import select
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
        print("En attente de connexion ...")
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('127.0.0.1',8000))
        self.sock.sendall(self.name.encode('ascii'))
        response = self.sock.recv(1024).decode('ascii')
        print("Bienvenue, %s ! :) \n" % response)
        print("Tapez 'start' pour lancer une partie")
        print("Tapez 'wait' pour attendre vos amis")
        print("Tapez 'quit' pour quiter le jeu")
        self.connected=True
        inp='1'
        try :
            while self.connected :
                if inp=='1' :
                    print(">")
                    i, o, e = select.select( [sys.stdin], [], [], 10 )
                    if (i):
                        line= sys.stdin.readline().strip()
                        line+="\x00"
                        if line == "quit\x00" : 
                            print("Fin de la connexion")
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
                    else:
                        inp=self.lire(self.sock)
                else : 
                    inp=self.lire(self.sock)
        except KeyboardInterrupt :
            print("Fin de la connexion")
            line = "quit\x00"
            self.sock.sendall(line.encode('ascii'))
        finally :
            self.sock.close()

    def lire(self,sock):
        res = '0' # entier (0 si pas de réponse attendue, 1 si réponse attendue, 3 si test connexion)
        response = sock.recv(1024).decode('ascii')
        if not response : 
            print("Le serveur a ete deconnecte")
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
    try:
        if len(sys.argv)>=2 :
                ch=sys.argv[1]
        else : 
            ch=input('Choisissez un pseudo > ')
        while ch=="" :
            print("Desole, ce pseudo n'est pas valide !")
            ch=input('Choisissez un pseudo > ')
        Client(ch)
    except KeyboardInterrupt :
        print("Fin de la connexion au serveur")
    except:
        print("Exception inatendue")
    finally :
        print("Merci d'avoir joue ! ^_^ ")
