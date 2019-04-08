Instructions de lancement
=========================

Il faut premièrement lancer le fichier Serveur.py (python3 Serveur.py) puis un ou plusieurs clients avec le fichier Client.py. 
En se connectant, chaque participant choisit son pseudo. Il est également possible de choisir son pseudo directement en lançant le fichier Client.py (Exemple: python3 Client.py pseudo). Dans ce cas le pseudo ne sera pas demandé. Enfin, pour une utilisation en réseau avec plusieurs machines, il faut fournir le pseudo ainsi que l'adresse IP de la machine sur laquelle le serveur a été lancé.

Il est possible de jouer en réseau sur n'importe quel ordinateur de l'INSA. Il faudra alors préciser l'adresse IP de l'ordinateur qui lance le serveur (Exemple: python3 Client.py pseudo 134.214.159.199). 

Pour obtenir l'adresse IP vous pouvez rentrer la commande suivante dans un terminal : "curl ifconfig.me". Si on ne précise pas d'adresse IP, le quiz se lancera en local.

