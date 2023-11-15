import numpy as np

class Ball():

    def __init__(self,number,initial_position,radius=0.0286,mass=0.162):
        self.number = number
        self.radius = radius #en m
        self.mass = mass #en kg
        self.position = initial_position
        self.speed = [0,0]
    
    def update_position(self,vecteur_position):
        self.position = vecteur_position
    
    def update_speed(self,vector_vitesse):
        self.speed = vector_vitesse
    
    def properties(self):
        return "La boule numéro "+str(self.number)+" se trouve à la position "+ str(self.position)+" et a un vecteur vitesse de "+str(self.speed)+"."
    


class Board():
    
    def __init__(self,length=2.54,width=1.27):
        self.length = length
        self.width = width
        self.corners = self.set_corners() #liste de 4 couples qui correspondent aux coordonnées des coins
        self.middle = self.set_middle()


    def set_corners(self):
        corner1 = [0,0]
        corner2 = [self.length,0]
        corner3 = [self.length,self.width]
        corner4 = [0, self.width]
        return [corner1,corner2,corner3,corner4]

    def set_middle(self):
        return [self.width/2,self.length/2]
    
    def properties(self):
        return "La table a une largeur "+str(self.width)+" et de longueur "+ str(self.length)+" a ses coins aux position "+str(self.corners)+" et son milieu se trouve aux coordonnées"+str(self.middle)+"."



class Cue():
    def __init__(self, mass):
        self.mass = mass
    
    def frappe(self, puissance, angle, ball): #puissance en J, angle en rad par rapport à l'axe x
        mcue = self.mass
        vcue = np.sqrt(2*puissance/mcue)
        mball = ball.mass
        vball = mcue/mball * vcue
        ball.update_speed([np.cos(angle)*vball, np.sin(angle)*vball])

B = Board()
bouleblanche = Ball(0, B.middle)
C = Cue(1)
C.frappe(50, 0, bouleblanche)
print(bouleblanche.properties())




        
