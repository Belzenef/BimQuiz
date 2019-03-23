#Elaboration d'un Quizz en réseau
Marie Codet, Alice Genestier, Elise Jacquemet, Cloé Mendoza
Projet réalisé dans le cadre du cours "Programmation réseau" de 4BIM.

Language utilisé: Python3

Le but de ce projet est de créer un quizz en réseau. Il faut premièrement lancer le fichier Serveur.py puis plusieurs clients avec le fichier Client.py. En se connectant, chaque participant choisit son pseudo. Il est également possible de choisir son pseudo directement en lancant le fichier Client.py (Exemple: python3 Client.py pseudo). Dans ce cas le pseudo ne sera pas demander.

Une fois connectés, les joueurs doivent choisir entre:
 * Attendre que d'autres joueurs se connectent ("wait")
 * Lancer une partie ("start")
 * Quitter le jeu ("quit")
 
Lorsqu'un joueur lance une partie, tout les joueurs en "attente" vont alors jouer. En lancant une partie, le joueur devra sélectionner un thème parmis 3 et choisir le nombre de questions souhaitées. Les joueurs répondront simultanément aux questions par vrai(V) ou faux(F). Si un joueur met trop de temps à répondre, il passe directement à la question suivante, sa réponse est donc considérée comme fausse. A la fin de la partie, les joueurs obtiennent le nombre de points gagnés ainsi que le classement de la partie. Ils reviennent alors au début et peuvent choisir d'attendre, de lancer une partie ou de quitter.
