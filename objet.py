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
        corner2 = [self.width,0]
        corner3 = [self.width,self.length]
        corner4 = [0, self.length]
        return [corner1,corner2,corner3,corner4]

    def set_middle(self):
        return [self.width/2,self.length/2]
    
    def properties(self):
        return "La table a une largeur "+str(self.width)+" et de longueur "+ str(self.length)+" a ses coins aux position "+str(self.corners)+" et son milieu se trouve aux coordonnées"+str(self.middle)+"."

B1 = Ball(1,[0,0])
print(B1.properties())

T = Board()
B1.update_position([1,1])
print(T.properties())