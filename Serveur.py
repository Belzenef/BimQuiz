import multiprocessing as mp
from multiprocessing import Queue, Manager, Process
from multiprocessing.sharedctypes import Value, Array
from socket import *
import select
from time import time, ctime
import sys
import signal
import traceback
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
        print("Lancement du serveur de Quizz")
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
        #try:
        pseudo = sockClient.recv(self.TAILLE_BLOC)
        pseudo=pseudo.decode("ascii")
        queue.put(pseudo)
        queue.put(sockClient)
        print("%s a rejoint le serveur" % pseudo)
        sockClient.sendall(pseudo.encode("ascii"))
        while connected:
            data = sockClient.recv(self.TAILLE_BLOC)
            data=data.decode('ascii')
            if not data :
                print("%s est deconnecte :'(" %pseudo)
                connected=False
            elif data ==  "quit\x00":
                print("%s a quitte le serveur :'(" %pseudo)
                connected=False
            elif data == "start\x00":
                if self.partie_en_cours.value==0 :
                    print("Lancement de la partie ...\n")
                    response="Vous avez lance une partie !0"
                    sockClient.sendall(response.encode("ascii"))
                    self.partie_en_cours.acquire()
                    self.partie_en_cours.value=1
                    self.partie_en_cours.release()
                    self.partie(queue,sockClient)
                else :
                    response="Une partie est deja en cours, merci de patienter :/1"
                    sockClient.sendall(response.encode("ascii"))
        #except:
            #print("Problem in request ?")
        #finally:
        sockClient.close()

    def partie(self, queue, lanceur):
        # Récupération des joueurs connectés
        queue.put("Done")
        response="La partie va commencer o/ \nVous avez 30sec pour repondre a chaque question ... \nBonne chance ! \n0"
        response=response.encode("ascii")
        joueurs={} # joueurs[sock]=(pseudo,score)
        print("Joueurs connectes : ")
        done=False
        nb_joueurs=0
        while not done :
            msg=queue.get()
            if msg=="Done" :
                done=True
            elif type(msg)==type(" ") :
                pseudo=msg
                sock=queue.get()
                score=0
                if self.connected(sock) :
                    sock.send(response)
                    joueurs[sock]=[pseudo,score]
                    nb_joueurs+=1
                    print(pseudo)
                else : 
                    print("%s est deconnecte :'(" %pseudo)

        # Récupération des questions
        tab = csv.reader(open("questions.csv","r", encoding ="utf-8"), dialect='excel-tab')
        quest=[]
        for row in tab: 
            quest.append(row)

        # Choix du thème
        

        # Choix du nb de questions
        msg="Combien de questions ? (max %d)\n1" % 10
        msg=msg.encode("ascii")
        lanceur.send(msg)
        rep=lanceur.recv(self.TAILLE_BLOC)
        rep=rep.decode('ascii')
        try :
            rep=int(rep[:-1]) # try catch pour eviter erreur
            if type(rep)==type(2) and rep<= 10 :
                nb_quest=rep
            else:
                nb_quest=3
        except :
            nb_quest=3
            pass

        # Selection des questions
        list_quest = [i for i in range(len(quest))]
        quest_al = random.sample(list_quest, nb_quest)

        # Déroulé du quizz
        count=1
        for i in quest_al:
            for sock in joueurs.keys():
                V_F="\nQuestion %d de %d: Repondez par Vrai (V) ou Faux (F)\n" % (count,nb_quest) 
                votre_rep="\nReponse:1"
                question=quest[i][1][:-1]
                sock.send(V_F.encode("ascii"))
                sock.send(question.encode("ascii"))
                sock.send(votre_rep.encode("ascii"))  
            print("Question %d posee" % count)
            nb_rep=0
            t = 0
            lus=[]
            while(nb_rep<nb_joueurs and t<10) :
                debut=time()
                try:
                    a_lire, wlist, xlist = select.select(joueurs.keys(),[], [], 10)
                except select.error:
                    print("select error")
                    pass
                else:
                    # On parcourt la liste des clients à lire
                    for sock in a_lire: # Client est de type socket
                        lus.append(sock)
                        answer = sock.recv(self.TAILLE_BLOC)
                        answer = answer.decode("ascii")
                        print(answer)
                        nb_rep+=1
                        if answer[0].capitalize() == quest[i][2]:
                            joueurs[sock][1] +=1
                            rep_joueur="Bravo !\n"
                        else:
                            rep_joueur="Perdu !\n"
                        sock.sendall(rep_joueur.encode("ascii"))
                fin=time()
                t+=fin-debut
            for sock in joueurs.keys() :
                if sock not in lus :
                    rep_joueur="Temps ecoule !\n"
                    sock.sendall(rep_joueur.encode("ascii"))
            print("Tous les joueurs ont repondu")
            count+=1
            
        # Affichage des scores
        for sock in joueurs.keys():
            score_tot="Bien joue ! Vous avez {0} point(s) !\n0" .format(joueurs[sock][1])
            sock.sendall(score_tot.encode("ascii"))

        # Fin de la partie
        self.partie_en_cours.acquire()
        self.partie_en_cours.value=0
        self.partie_en_cours.release()
        response="Merci d'avoir joue ;)\n1"
        response=response.encode("ascii")
        for sock in joueurs.keys():
            queue.put(joueurs[sock][0])
            queue.put(sock)
            sock.send(response)
        print("Fin de la partie ...\n")

    def connected(self,sock):
        res=False
        ch="test3"
        ch=ch.encode('ascii')
        sock.send(ch)
        data = sock.recv(self.TAILLE_BLOC).decode('ascii')
        if data=="test" :
            res=True
        return(res)  
 
if __name__ == "__main__":
        try:
            Serveur()
        except KeyboardInterrupt :
            print("Fermeture du serveur")
        except:
            print("Exception inattendue")
        finally:
            for process in mp.active_children():
                print("Fermeture du processus ", process)
                process.terminate()
                process.join()
            print("FIN")


# https://pytorch.org/docs/stable/notes/multiprocessing.html
#https://realpython.com/python-sockets/
#https://github.com/JustinTulloss/zeromq.node/issues/163
#https://bugs.python.org/issue4892