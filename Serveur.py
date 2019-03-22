import multiprocessing as mp
from multiprocessing import Queue, Manager, Process
from multiprocessing.sharedctypes import Value, Array
from socket import *
import select
from time import time, ctime
import sys
import signal
import traceback
import re
import csv
import random

comSocket = socket(AF_INET, SOCK_STREAM)
comSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


class Serveur:
    def __init__(self):
        # Initialisation de la classe """
        self.TAILLE_BLOC=1024 # la taille des blocs 
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(("127.0.0.1",8000))
        self.sock.listen(5)
        self.partie_lancee=Value('i', 0)
        self.partie_en_cours=Value('i', 0)
        self.queue = Manager().Queue()
        print("Welcome to the best Quiz ever! ")
        self.run()

    def run(self):
        while True:
            con, addr = self.sock.accept()
            process = mp.Process(target=self.handle_conn, args=(con, addr, self.queue))
            process.daemon = True
            process.start()
        self.sock.close()
        
    def handle_conn(self, sockClient, addr, queue):
        connected = True
#<<<<<<< HEAD
#        try:
#            pseudo = sockClient.recv(self.TAILLE_BLOC)
#            pseudo=pseudo.decode("ascii")
#            queue.put(pseudo)
#            queue.put(sockClient)
#            print("%s joined server" % pseudo)
#            sockClient.sendall(pseudo.encode("ascii"))
#            while connected:
#                data = sockClient.recv(self.TAILLE_BLOC)
#                data=data.decode('ascii')
#                if not data :
#                    print("%s is disconnected :'(" %pseudo)
#                    connected=False
#                if data ==  "quit\x00":
#                    print("%s has left server :'(" %pseudo)
#                    connected=False
#                elif data == "start\x00":
#                    if self.partie_en_cours.value==0 :
#                        print("Starting game ...")
#                        response="You started a new game !0"
#                        sockClient.sendall(response.encode("ascii"))
#                        self.partie_en_cours.acquire()
#                        self.partie_en_cours.value=1
#                        self.partie_en_cours.release()
#                        #game = mp.Process(target=self.partie, args=(queue))
#                        #game.daemon = True
#                        #game.start()
#                        #game.join()
#                        self.partie(queue)
#                    else :
#                        response="Game already started :/0"
#                        sockClient.sendall(response.encode("ascii"))
#        except:
#            print("Problem in request ?")
#        finally:
#            sockClient.close()
#
#    def partie(self, queue):
#        print("hey")
#        # Recuperation des joueurs connectes
#=======
        #try:
        pseudo = sockClient.recv(self.TAILLE_BLOC)
        pseudo=pseudo.decode("ascii")
        queue.put(pseudo)
        queue.put(sockClient)
        print("%s joined server" % pseudo)
        sockClient.sendall(pseudo.encode("ascii"))
        while connected:
            data = sockClient.recv(self.TAILLE_BLOC)
            data=data.decode('ascii')
            if not data :
                print("%s is disconnected :'(" %pseudo)
                connected=False
            elif data ==  "quit\x00":
                print("%s has left server :'(" %pseudo)
                connected=False
            elif data == "start\x00":
                if self.partie_en_cours.value==0 :
                    print("Starting game ...")
                    response="You started a new game !0"
                    sockClient.sendall(response.encode("ascii"))
                    self.partie_en_cours.acquire()
                    self.partie_en_cours.value=1
                    self.partie_en_cours.release()
                        #game = multiprocessing.Process(target=self.partie, args=(queue))
                        #game.daemon = True
                        #game.start()
                        #game.join()
                    self.partie(queue)
                else :
                    response="Game already started :/0"
                    sockClient.sendall(response.encode("ascii"))
        #except:
            #print("Problem in request ?")
        #finally:
        sockClient.close()

    def partie(self, queue):
        print("hey")
        # Récupération des joueurs connectés
        queue.put("Done")
        response="Welcome to the party o/ 0"
        response=response.encode("ascii")
        joueurs={} # joueurs[sock]=(pseudo,score)
        print("Connected players : ")
        done=False
        while not done :
            msg=queue.get()
            print("elt queue : ",msg)
            if msg=="Done" :
                done=True
            elif type(msg)==type(" ") :
                pseudo=msg
                sock=queue.get()
                score=0
                if self.connected(sock) :
                    sock.send(response)
                    rep=""
                    joueurs[sock]=(pseudo,score)
                    print("joueur :",pseudo)
                else : 
                    print("%s is disconnected :'(" %pseudo)           
            #else :
                #pseudo="Unknown"
                #sock=msg
                #score=0
                #if self.connected(sock) :
                     #sock.send(response)
                    #joueurs[sock]=(pseudo,score)
                    #print("joueur :",pseudo)
                #else : 
                    #print("%s is deconnected :'(" %pseudo) 
                    
        # Récupération des questions
        tab = csv.reader(open("question_quizz.csv","r", encoding ="utf-8"), dialect='excel-tab')
        quest=[]
        for row in tab: 
            quest.append(row)
        nb_quest=2
        list_quest = [i for i in range(len(quest))]
        quest_al = random.sample(list_quest, nb_quest)
        # Déroulé du quizz
        for i in quest_al:
            for sock in joueurs.keys():
                V_F="\nV ou F ?\n"
                votre_rep="Votre reponse:1"
                question=quest[i][1][:-1]
                sock.send(question.encode("ascii"))
                sock.send(V_F.encode("ascii"))
                sock.send(votre_rep.encode("ascii"))  
                #print("jhfdkhgkjfdhgsj")        
                answer=sock.recv(self.TAILLE_BLOC)
                #print("youhou")
                #answer=answer.decode('ascii')  
                #print(answer[0] == quest[i][2])
                print(type(answer[0]))
                if answer[0].capitalize() == quest[i][2]:
                    #print("blavlia")
                    joueurs[sock][1] +=1
                    rep_joueur="Bien ouej!\n"
                else:
                    #print("blaglikjfdhgjfshiufsl")
                    rep_joueur="Bah non patate\n"
                sock.sendall(rep_joueur.encode("ascii"))
            
        # Affichage des scores
            
        for sock in joueurs.keys():
            score_tot="Bravo ! Vous avez {0} points!\n0" .format(joueurs[sock][1])
            sock.sendall(score_tot.encode("ascii"))
          
        # Fin de la partie
        self.partie_en_cours.acquire()
        self.partie_en_cours.value=0
        self.partie_en_cours.release()
        response="Thanks for playing ;)\n1"
        response=response.encode("ascii")
        for sock in joueurs.keys():
            queue.put(joueurs[sock][0])
            queue.put(sock)
            sock.send(response)
            print("\n")

    def connected(self,sock):
        res=False
        ch="test3"
        ch=ch.encode('ascii')
        sock.send(ch)
        data = sock.recv(self.TAILLE_BLOC).decode('ascii')
        print(data)
        if data=="test" :
            res=True
        return(res)  
 
if __name__ == "__main__":
        try:
            Serveur()
        except KeyboardInterrupt :
            print("Shutting down server")
        except:
            print("Unexpected exception")
        finally:
            for process in mp.active_children():
                print("Shutting down process ", process)
                process.terminate()
                process.join()
            print("END")


# https://pytorch.org/docs/stable/notes/multiprocessing.html
#https://realpython.com/python-sockets/
#https://github.com/JustinTulloss/zeromq.node/issues/163
#https://bugs.python.org/issue4892