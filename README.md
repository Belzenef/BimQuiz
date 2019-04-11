# BIMQUIZ

## Elaboration d'un Quizz en réseau

Le but de ce projet est de créer un quizz en réseau entre plusieurs participants. Des centaines de questions amusantes, sur des thèmes variés tels que lec chats, la musique ou les mots & expressions !
 
Une fois le serveur TCP lancé, autant de joueurs que souhaité peuvent se connecter. 
Mais si vous voulez utiliser ce quiz en solo, c'est également possible !

Une fois connectés, les joueurs doivent choisir entre:
 * Attendre que d'autres joueurs se connectent ("wait") 
 * Lancer une partie ("start")
 * Quitter le jeu ("quit")
 
Si la saisie du client est invalide ou s'il ne répond pas au bout de 30 secondes, cela aura le même effet que "wait".
 
Lorsqu'un joueur lance une partie, tout les joueurs en attente vont alors se joindre à lui pour répondre aux questions. En lançant une partie, le joueur devra d'abord sélectionner un thème parmis 3 proposés aléatoirement et choisir le nombre de questions souhaitées. 

Les joueurs répondront simultanément aux questions par vrai ou faux. Mais attention, le temps est limité ! Si un joueur met plus de 30 secondes à répondre il passe directement à la question suivante et ne gagne aucun point :'(

A la fin de la partie, les joueurs obtiennent le nombre de points gagnés ainsi que le classement de la partie. 

Les points sont comptés de la façon suivante:
  * +1 si le joueur répond correctement à la question
  * -0.5 si le joueur donne une mauvaise réponse
  * 0 s'il ne répond pas
   
A l'issue du classement, les utilisateurs reviennent au choix initial et peuvent alors attendre, lancer une partie ou quitter le serveur.

Amusez vous bien !

## Installation

Vous pouvez cloner le repository disponible sur Github [ici](https://github.com/Belzenef/Quizz/)

Ou bien utiliser le projet PyPI déposé  [ici](https://test.pypi.org/project/Bimquizz/)

## Instructions

Il faut premièrement lancer le fichier Serveur.py (python3 Serveur.py) puis un ou plusieurs clients avec le fichier Client.py. 
En se connectant, chaque participant choisit son pseudo. Il est également possible de choisir son pseudo directement en lançant le fichier Client.py (Exemple: python3 Client.py pseudo). Dans ce cas le pseudo ne sera pas demandé. Enfin, pour une utilisation en réseau avec plusieurs machines, il faut fournir le pseudo ainsi que l'adresse IP de la machine sur laquelle le serveur a été lancé.

Il est possible de jouer en réseau sur n'importe quel ordinateur de l'INSA. Il faudra alors préciser l'adresse IP de l'ordinateur qui lance le serveur (Exemple: python3 Client.py pseudo 134.214.159.199). 

Pour obtenir l'adresse IP vous pouvez rentrer la commande suivante dans un terminal : "curl ifconfig.me". Si on ne précise pas d'adresse IP, le quiz se lancera en local.

## Améliorations

La version actuelle ne permet pas de lancer plusieurs parties en même temps, que ce soit avec des joueurs différents ou bien avec des joueurs déjà impliqués dans une partie. Dans l'idéal, nous aimerions pouvoir lancer plusieurs parties simultanées sur des thèmes différents, et proposer aux joueurs de rejoindre l'une des parties lancées.

Nous souhaiterions également à terme ajouter différent types de questions de type QCM ou questions libres.

Une interface graphique pourrait également être développée, car pour le moment tous les affichages sont dans le terminal. Nous pourrions ainsi également proposer un affichage des joueurs actuellement connectés afin que l'utilisateur puisse s'assurer que tous les participants soient connectés avant de lancer la partie.

## FAQ

* __Je n'arrive pas a me connecter au serveur__ :
Vérifiez que le serveur a bien été lancé AVANT de lancer un script Client. Si vous  souhaitez jouer en réseau, vérifiez que vous avez saisi correctement l'addresse IP d'où a été lancé le serveur. (Exemple: python3 Client.py pseudo 134.214.159.199). 

-----------------

* __J'ai lancé une partie mais mes amis ne peuvent pas la rejoindre__ :
Attention ! il faut bien attendre que tout le monde soit connecté au serveur et ait saisi "wait" AVANT de lancer la partie.

-----------------

* __Le serveur ne compte pas mes points correctement__ :
Vérifiez que vous entrez bien "v" ou "f" (majuscules ou non, comme vous voulez !) pour répondre et non autre chose

-----------------

Pour d'autres questions, n'hésitez pas à contacter nous contacter : elise.jacquemet@insa-lyon.fr

## Pour aller plus loin ...

Lien vers la [documentation](https://readthedocs.org/projects/quizz/)

Language utilisé: python3

Projet réalisé dans le cadre du cours "Programmation réseau" de 4BIM.

