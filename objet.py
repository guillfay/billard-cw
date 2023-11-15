class Boule():

    def __init__(self,numero,position_initiale):
        self.number = numero
        self.radius = 0.0286 #en m
        self.mass = 0.162 #en kg
        self.position = position_initiale
        self.vitesse = [0,0]
        self.acceleration = [0,0]
    
    def update_position(self,vecteur_position):
        self.position = vecteur_position
    
    def update_vitesse(self,vecteur_vitesse):
        self.vitesse = vecteur_vitesse
    
    def properties(self):
        return "La boule numéro "+str(self.number)+" se trouve à la position "+ str(self.position)+" et a un vecteur vitesse de "+str(self.vitesse)+"."

class Bord():
    
    def __init__(extremites):
        self.


B1 = Boule(1,[0,0])
print(B1.properties())
