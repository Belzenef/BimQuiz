class Partie:
    
    def __init__(self, pseudo, score, questions):
        self.pseudo = pseudo #chaîne de caractères
        if type (pseudo) is not str :
            print("l'attribut pseudo doit être une chaîne de caractère")
        self.score = score #nombre
        self.questions = questions #liste de nombre

partie1= Partie("toto", 25, [12,3,45,9])
print("Le pseudo est : ", partie1.pseudo)
print("le score est : ", partie1.score)
print("la liste des questions est : ", partie1.questions)

