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

# Pour éviter l'erreur récurente "port already in use" lors des arrets 
# repetés de vos codes serveurs, utiliser l'option socket suivante: 

comSocket = socket(AF_INET, SOCK_STREAM)
comSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


class Serveur:
    def __init__(self):
        # Initialisation de la socket serveur
        self.TEMPS_MAX=30
        self.TAILLE_BLOC=4096
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock .setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock .setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.sock.bind(("",8000))
        self.sock.listen(26)

         # Attributs
        self.partie_en_cours=Value('i', 0)
        self.manager= Manager()
        self.connexions = self.manager.dict() # clients connectés au serveur
        self.data = self.manager.Queue() # Queue pour les communications entre processus

        print("Lancement du serveur de Quizz")
        self.run()

    def run(self):
        while True:
            con, addr = self.sock.accept()
            process = mp.Process(target=self.handle_conn, args=(con,addr))
            process.daemon = False
            process.start()
        self.sock.close() # Fermeture du serveur
        
    def handle_conn(self, sockClient, addrClient):
        connected = True
        #try:
        # Attribution du pseudo au client et ajout à la liste des connexions
        pseudo = sockClient.recv(self.TAILLE_BLOC)
        pseudo=pseudo.decode("ascii")
        while pseudo in self.connexions.keys() :
            pseudo+=str(random.randint(1,100))
        self.connexions[pseudo]=(sockClient,0)
        print("%s a rejoint le serveur" % pseudo)
        sockClient.sendall(pseudo.encode("ascii"))

        # Lancement des communications client/serveur
        while connected:
            msg = sockClient.recv(self.TAILLE_BLOC)
            msg=msg.decode('ascii')
            if len(msg)>0 :
                nouvJoueur=msg[-1]=="!"
                if msg[:-1] ==  "quit": # deconnexion côté client
                    print("%s a quitte le serveur :'(" %pseudo)
                    reponse="quit"
                    connected=False
                elif msg == "start!": # un nouveau client lance une partie
                    # Si aucune partie en cours
                    if self.partie_en_cours.value==0 :
                        print("Lancement de la partie ...\n")
                        reponse="\nVous avez lance une partie !"
                        self.partie_en_cours.acquire()
                        self.partie_en_cours.value=1
                        self.partie_en_cours.release()
                        game = mp.Process(target=self.partie, args=(pseudo,sockClient))
                        game.daemon = True
                        game.start()
                    # Si une partie a dejà été lancée auparavant
                    else :
                        reponse="Une partie est deja en cours, merci de patienter :/"
                else : # message quelconque 
                    reponse="Veuillez patienter..."
                if nouvJoueur :
                    print("data : ", msg)
                    self.envoyer(self.connexions[pseudo][0],reponse)
                else :
                    self.data.put(pseudo)
                    self.data.put(sockClient)
                    self.data.put(msg)
            else :
                print("%s est deconnecte :'(" %pseudo)
                connected=False
        #except:
            #print("Problem in request ?")
        #finally:
        del self.connexions[pseudo]
        sockClient.close()

    def partie(self, lanceur, sockLanceur):
        # Récupération des joueurs connectés
        # connexions.put("Done")
        consigne="La partie va commencer o/ \nVous avez 30sec pour repondre a chaque question ... \nBonne chance ! \n"
        debut="Debut Partie"
        joueurs={} # joueurs[pseudo]=(socket,score)
        print("Joueurs connectes : ")
        for pseudo in self.connexions.keys() :
            sockJoueur=self.connexions[pseudo][0]
            scoreJoueur=self.connexions[pseudo][1]
            joueurs[pseudo]=[sockJoueur,scoreJoueur]
            self.envoyer(joueurs[pseudo][0],consigne)
            self.envoyer(joueurs[pseudo][0],debut)
            print(pseudo)
        nb_joueurs=len(joueurs)
        print("Au total, %s joueur(s) sont connectes" % nb_joueurs)

        if nb_joueurs==0 :
            self.partie_en_cours.acquire()
            self.partie_en_cours.value=0
            self.partie_en_cours.release()
            print("Fin de la partie ...\n")
            return 
        
        # Récupération des questions
        tab = csv.reader(open("question_quizz.csv","r", encoding ="utf-8"), dialect='excel-tab')
        count = 0
        quest ={}
        for row in tab:
            if count ==0:
                quest[row[0]] = [] 
            quest[row[0]].append([row[1],row[2]])
            count +=1
            
            if count == 10:
                count =0

        # Choix du thème
        print("\nChoix du theme")
        choix_theme=random.sample(quest.keys(),3)
        msg="Entrer le theme de votre choix parmis ces trois : %s, %s et %s" %(choix_theme[0],choix_theme[1],choix_theme[2])
        if self.connected(lanceur) :
            self.demander(joueurs[lanceur][0],msg)
            succes,pseudo,sock,reponse = self.lire_queue()
            print(succes)
            print(reponse)
            if succes :
                reponse=reponse[:-1].lower()
                if reponse == "quit" :
                    print("Deconnexion inattendue")
                    self.retirer(joueurs,lanceur)
                    theme = random.sample(quest.keys(),1)[0]
                    print("Theme aleatoire : ", theme)
                elif reponse in choix_theme :
                    print("%s a choisi le theme %s " % (pseudo,reponse))
                    theme = reponse
                else:
                    theme = random.sample(quest.keys(),1)[0]
                    msg="Vous avez fait n'importe quoi alors on vous donne un theme aleatoire : %s" %theme
                    self.envoyer(joueurs[lanceur][0],msg)
                    print("Theme aleatoire : ", theme)
            else :
                print("Deconnexion inattendue")
                self.retirer(joueurs,lanceur)
                theme = random.sample(quest.keys(),1)[0]
                print("Theme aleatoire : ", theme)
        else :
            print("Deconnexion inattendue")
            self.retirer(joueurs,lanceur)
            theme = random.sample(quest.keys(),1)[0]
            print("Theme aleatoire : ", theme)
        
        # MAJ du nombre de joueur au cas où le lanceur se deconnecte
        nb_joueurs=len(joueurs)
        if nb_joueurs==0 :
            self.partie_en_cours.acquire()
            self.partie_en_cours.value=0
            self.partie_en_cours.release()
            print("Fin de la partie ...\n")
            return 

        # Choix du nb de questions
        print("\nChoix du nombre de questions")
        msg="Combien de questions ? (max %d)\n" %len(quest[theme])
        if self.connected(lanceur) :
            self.demander(joueurs[lanceur][0],msg)
            succes,pseudo,sock,reponse = self.lire_queue()
            if succes :
                if reponse == "quit\x00" :
                    print("Deconnexion inattendue")
                    self.retirer(joueurs,lanceur)
                    nb_quest=3
                else :
                    try :
                        rep=int(reponse[:-1])
                    except :
                        rep=3
                        msg="Vous avez rentre un nombre incorrect ! Nombre de questions par default : %s" %rep
                        self.envoyer(joueurs[lanceur][0],msg)
                        pass
                    if type(rep)==type(2) and rep<=len(quest[theme]) :
                        print("%s a choisi %s questions" % (pseudo,rep))
                        nb_quest=rep
                    else:
                        nb_quest=3
                        msg="Vous avez rentre un nombre incorrect ! Nombre de questions par default : %s" %nb_quest
                        self.envoyer(joueurs[lanceur][0],msg)
            else :
                print("Deconnexion inattendue")
                self.retirer(joueurs,lanceur)
                nb_quest=3
        else :
            print("Deconnexion inattendue")
            self.retirer(joueurs,lanceur)
            nb_quest=3
        print("nb quest ",nb_quest)
        nb_joueurs=len(joueurs)
        
        # MAJ du nombre de joueur au cas où le lanceur se deconnecte
        if nb_joueurs==0 :
            self.partie_en_cours.acquire()
            self.partie_en_cours.value=0
            self.partie_en_cours.release()
            print("Fin de la partie ...\n")
            return 

        # Selection des questions
        nb_quest_theme = [i for i in range(len(quest[theme]))]
        index_al = random.sample(nb_quest_theme, nb_quest)

        # Déroulé du quizz
        count=1
        print("\nLancement du Quizz avec %s joueur(s)" % nb_joueurs)
        for i in index_al : # parcourir la liste de questions
            # boucle pour poser la question à tous les joueurs
            for pseudo in joueurs.keys() :
                V_F="\nQuestion %d de %d: Repondez par Vrai (V) ou Faux (F)" % (count,nb_quest) 
                votre_rep="\nReponse:"
                question=quest[theme][i][0][:-1]
                if self.connected(pseudo) :
                    self.envoyer(joueurs[pseudo][0],V_F)
                    self.envoyer(joueurs[pseudo][0],question)
                    self.demander(joueurs[pseudo][0],votre_rep)
            print("Question %d posee" % count)

            # boucle pour attendre les réponses
            t = 0
            reponses={}
            debut=time()
            while(len(reponses)<nb_joueurs and t<self.TEMPS_MAX) : # temps écoulé ou tous les joueurs répondent
                succes,pseudo,sock,reponse = self.lire_queue()
                if succes :
                    joueurs[pseudo][0]=sock
                    reponses[pseudo]=reponse[:-1]
                    if reponses[pseudo]!="quit" :
                        print("%s a repondu %s " % (pseudo,reponses[pseudo]))
                else :
                    print("Deconnexion inattendue")

            nouvJoueurs={} # MAJ des joueurs en cas de déconnexion imprévue
            for pseudo in joueurs.keys() :
                if pseudo in reponses :
                    repJoueur = reponses[pseudo]
                    if len(repJoueur)>0 :
                        if repJoueur == "quit" :
                            print("Deconnexion inattendue")
                        elif repJoueur=="none" :
                            print("%s n'a pas repondu a temps" % pseudo)
                            resultat="Temps ecoule !"
                        elif repJoueur[0].capitalize() == quest[theme][i][1]:
                            joueurs[pseudo][1] +=1 # augmentation du score
                            resultat="Bravo !"
                        else:
                            resultat="Perdu !"
                    else:
                        print("Reponse invalide de %s" % pseudo)
                        resultat="Reponse invalide !"
                if self.connected(pseudo) :
                    self.envoyer(joueurs[pseudo][0],resultat)
                    nouvJoueurs[pseudo]=[joueurs[pseudo][0],joueurs[pseudo][1]]
                else :
                    nb_joueurs-=1

            # MAJ du nombre de joueur au cas où tous les joueurs soient deconnectes
            if nb_joueurs==0 :
                print("Plus de joueurs en jeu !")
                break
            print("Scores enregistres")
            joueurs=nouvJoueurs.copy()
            count+=1

        # MAJ du nombre de joueur au cas où le lanceur se deconnecte
        print("nb joueurs : " , nb_joueurs)
        if nb_joueurs==0 :
            self.partie_en_cours.acquire()
            self.partie_en_cours.value=0
            self.partie_en_cours.release()
            print("Fin de la partie ...\n")
            return 

        # Creation du classement
        print("\nClassement des joueurs")
        classment = joueurs.items()

        classement_trie = sorted(classment, key=lambda x: x[1][1])
        classement_trie.reverse()
        pod = []
        for i in range(len(classement_trie)):
            pod.append("%d : %s" %(i+1, classement_trie[i][0]))

        # Affichage des scores et du classement final
        for pseudo in joueurs.keys():
            if self.connected(pseudo):
                if joueurs[pseudo][1] == 0:
                    score_tot = "Bah alors on a pas reussi a marquer un seul point??"
                else:
                    score_tot="Bien joue ! Vous avez {0} point(s) !" .format(joueurs[pseudo][1])
                self.envoyer(joueurs[pseudo][0],score_tot)
    
                podium = "\nClassement de la partie :"
                self.envoyer(joueurs[pseudo][0],podium)
                for i in pod:
                    self.envoyer(joueurs[pseudo][0],i)

        # Fin de la partie
        self.partie_en_cours.acquire()
        self.partie_en_cours.value=0
        self.partie_en_cours.release()
        merci="\nMerci d'avoir joue ;)"
        rejouer="Que voulez vous faire ?\n"
        fin="Fin Partie"
        for pseudo in joueurs.keys():
            if self.connected(pseudo) :
                self.envoyer(joueurs[pseudo][0],merci)
                self.envoyer(joueurs[pseudo][0],fin)
                self.demander(joueurs[pseudo][0],rejouer)
        print("Fin de la partie ...\n")

    def connected(self,pseudo):
        print('test connexion %s : %s' %(pseudo,pseudo in self.connexions))
        return(pseudo in self.connexions)

    def retirer(self,joueurs,pseudo):
        try :
            del joueurs[pseudo]
            print("%s ne fait plus partie des joueurs" % pseudo)
        except :
            print("%s a deja ete retire" % pseudo)
            pass

    def envoyer(self,sock,msg): # envoi d'un message à afficher au client
        res=False
        try :
            msg=msg.encode('ascii')
            #sock=self.connexions[pseudo][0]
            sock.send(msg)
            res=True
        except :
            res=False
            pass
        return res

    def demander(self,sock,msg): # envoi d'un message attendant une réponse
        res=False
        try :
            msg+='1'
            msg=msg.encode('ascii')
            #sock=self.connexions[pseudo][0]
            sock.send(msg)
            res=True
        except :
            res=False
            pass
        return res

    def lire_queue(self) :
        succes = False
        try:
            pseudo=self.data.get() # pseudo
            sock=self.data.get() # socket
            reponse=self.data.get() # message
            succes=True
        except :
            succes=False
            pass
        return succes,pseudo,sock,reponse


if __name__ == "__main__":
        Serveur()
#        try:
#            Serveur()
#        except KeyboardInterrupt :
#            print("Fermeture du serveur")
#        except:
#            print("Exception inattendue")
#        finally:
#            for process in mp.active_children():
#                print("Fermeture du processus ", process)
#                process.terminate()
#                process.join()
#            print("FIN")