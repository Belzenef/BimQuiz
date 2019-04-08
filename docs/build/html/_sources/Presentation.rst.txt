Elaboration d'un Quizz en réseau
================================

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

