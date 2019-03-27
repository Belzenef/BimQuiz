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
    def __init__(self,ch,addr):
        # Attributs
        self.TEMPS_MAX=30
        self.TAILLE_BLOC=4096 
        self.name = ch
        self.connected=False
        
        # Connexion au serveur
        print("En attente de connexion ...")
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock .setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock .setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.sock.connect((addr,8000))
        self.sock.sendall(self.name.encode('ascii'))
        self.name = self.sock.recv(self.TAILLE_BLOC).decode('ascii')
        print("Bienvenue, %s ! :) \n" % self.name)
        print("Tapez 'start' pour lancer une partie")
        print("Tapez 'wait' pour attendre vos amis")
        print("Tapez 'quit' pour quiter le jeu")

        self.connected=True
        self.playing=False # le client connecté n'est pas encore dans une partie
        inp=True # bool permettant de demander à l'utilisateur de saisir au clavier
        try :
            while self.connected :
                if inp : # Si le serveur demande une communication
                    print(">")
                    i, o, e = select.select( [sys.stdin], [], [], self.TEMPS_MAX )

                    if self.playing : # client en train de jouer
                        if (i):
                            line= sys.stdin.readline().strip()
                            line+="\x00"
                            if line == "quit\x00" : 
                                print("Fin de la connexion")
                                self.sock.sendall(line.encode('ascii'))
                                self.connected=False
                            else :
                                line=line.encode('ascii')
                                self.sock.sendall(line)
                                inp=self.lire(self.sock)
                        else: # si pas d'activité au bout de 30sec, retour à un etat de lecture
                            line="none\x00".encode('ascii')
                            self.sock.sendall(line)
                            inp=self.lire(self.sock)

                    else : # nouveau client
                        if (i):
                            line= sys.stdin.readline().strip()
                            line+="!"
                            if line == "quit!" : 
                                print("Fin de la connexion")
                                self.sock.sendall(line.encode('ascii'))
                                self.connected=False
                            elif line == "start!" : 
                                self.sock.sendall(line.encode('ascii'))
                                inp=self.lire(self.sock)
                                self.playing=True
                            else :
                                line=line.encode('ascii')
                                self.sock.sendall(line)
                                inp=self.lire(self.sock)
                        else: # si pas d'activité au bout de 30sec, retour à un etat de lecture
                            line="none!".encode('ascii')
                            self.sock.sendall(line)
                            inp=self.lire(self.sock)

                else : # si pas de communication attendue, lecture simple du serveur
                    inp=self.lire(self.sock)

        except KeyboardInterrupt : # interruption clavier côté client
            print("Fin de la connexion")
            line = "quit\x00"
            self.sock.sendall(line.encode('ascii'))
        finally :
            self.sock.close()

    def lire(self,sock):
        reponse = sock.recv(self.TAILLE_BLOC).decode('ascii')
        res=False
        if len(reponse)>0 :
            if reponse=='Debut Partie' : # debut de partie
                self.playing=True
            elif reponse=='Fin Partie' : # fin de partie
                self.playing=False
            elif reponse[-1]=='1' :
                print(reponse[:-1])
                res=True
            else : 
                print(reponse)
        else :
            print("Le serveur a ete deconnecte")
            self.connected=False
        return res

if __name__ == "__main__":
    try:
        if len(sys.argv)>=3:
                ch=sys.argv[1]
                addr=sys.argv[2]
        elif len(sys.argv)>=2:
                ch=sys.argv[1]
                addr="127.0.0.1"
        else : 
            ch=input('Choisissez un pseudo > ')
            addr="127.0.0.1"
        while ch=="" :
            print("Desole, ce pseudo n'est pas valide !")
            ch=input('Choisissez un pseudo > ')
        Client(ch,addr)
    except KeyboardInterrupt :
        print("Fin de la connexion au serveur")
    except:
        print("Exception inatendue")
    finally :
        print("Merci d'avoir joue ! ^_^ ")