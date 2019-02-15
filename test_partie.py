import csv
import random


tab = csv.reader(open("question_quizz.csv","r", encoding ="utf-8"), dialect='excel-tab')
quest=[]

for row in tab: 
  quest.append(row)

print(quest[0])

nb_quest=2

liste_quest = [i for i in range(len(quest))]
quest_al = random.sample(liste_quest, 2)

compteur=0
for i in quest_al:
  print (quest[i][1])
  print ("V ou F ?")
  answer=input('Votre reponse:')
  if answer == quest[i][2]:
    print ("Bien ouej!")
    compteur+=1
  else:
    print ("Bah non patate")
  print("\n")
  input("Appuyez sur une touche pour passer à l'étape suivante ")
  print("\n")

print("Bravo ! Vous avez cummulé {0} points!" .format(compteur))

  
  


              




