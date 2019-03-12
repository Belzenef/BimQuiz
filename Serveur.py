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
        self.TAILLE_BLOC=1024 # la taille des blocs 
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(("127.0.0.1",8000))
        self.sock.listen(5)
        self.partie_lancee=Value('i', 0)
        self.partie_en_cours=Value('i', 0)
        self.queue = Queue()
        print("Welcome to the best Quiz ever! ")
        self.run()

    def run(self):
        while True:
            con, addr = self.sock.accept()
            process = Process(target=self.handle_com, args=(con, addr, self.queue))
            process.daemon = True
            process.start()
        self.sock.close()

        
    def handle_com(self, sockClient, addr, queue):
        connected = True
        try:
            pseudo = sockClient.recv(self.TAILLE_BLOC)
            pseudo=pseudo.decode("ascii")
            queue.put(pseudo)
            queue.put(sockClient)
            print("%s joined server" % pseudo)
            sockClient.sendall(pseudo.encode("ascii"))
            while connected:
                data = sockClient.recv(self.TAILLE_BLOC)
                data=data.decode('ascii')
                if data ==  "quit\x00":
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
#                        game = multiprocessing.Process(target=self.partie, args=(queue))
#                        game.daemon = True
#                        game.start()
                        self.partie(queue)
                    else :
                        response="Game already started :/0"
                        sockClient.sendall(response.encode("ascii"))
        except:
            print("Problem in request ?")
        finally:
            sockClient.close()

    def partie(self, queue):
        
        # Récupération des joueurs connectés
        queue.put("Done")
        response="Welcome to the party o/ 0"
        response=response.encode("ascii")
        joueurs={} # joueurs[sock]=(pseudo,score)
        print("Connected players : ")
        while True :
            msg=queue.get()
            print("elt queue : ",msg)
            if msg=="Done" :
                break
            elif type(msg)==type("") :
                pseudo=msg
                sock=queue.get()
                score=0
                try : 
                    sock.send(response)
                    joueurs[sock]=(pseudo,score)
                    print("joueur :",pseudo)
                except : 
                    print("%s already left :/" % pseudo)           
                    pass 
            else :
                pseudo="Unknown"
                sock=msg
                score=0
                try : 
                    sock.send(response)
                    joueurs[sock]=(pseudo,score)
                    print("joueur :",pseudo)
                except : 
                    print("%s already left :/" % pseudo)           
                    pass 
                
        
        # Récupération des questions
        
        # Déroulé du quizz
        
        # Affichage des scores
        
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
 
if __name__ == "__main__":
        try:
            Serveur()
        except KeyboardInterrupt :
            print("Shutting down server")
        except:
            print("Unexpected exception")
        finally:
            for process in active_children():
                print("Shutting down process ", process)
                process.terminate()
                process.join()
            print("END")
