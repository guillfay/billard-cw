import objet as objet
import dynamic as dynamic
import numpy as np

def update_pool(pool,deltaT):
    #version sans interactions entre les boules et sans frottements
    number_of_balls = pool.number_of_balls
    balls = pool.balls
    width = pool.board.corners[3][0]
    length = pool.board.corners[3][1]
    virtual_position_matrix = np.zerros(number_of_balls)
    for ball in balls.values():
        virtual_position = ball.position + deltaT*ball.speed 
        

def on_the_board(position_vector,width,length):
    if position_vector[0] > width or position_vector[0] < 0 :
        return False
    if position_vector[1] > length or position_vector[1] < 0 :
        return False
    return True

def exit_border(virtual_position, width, length, ball):
    radius = ball.radius
    bottom_border = False
    top_border = False
    left_border = False
    right_border = False
    if virtual_position[1] < radius:
        bottom_border_border = True
    if virtual_position[0] < width - radius:
        right_border = True
    if virtual_position[0] < length - radius:
        top_border = True
    if virtual_position[0] < radius :
        left_border = True
    return [bottom_border,right_border,top_border,left_border]

def update_real_pool(pool,deltaT):
    #version sans frottements
    balls = pool.balls
    width = pool.board.corners[3][0]
    length = pool.board.corners[3][1]
    matrix = np.zerros((number_of_balls,number_of_balls))
    for ball in balls.values():
        virtual_position = ball.position + deltaT*ball.speed 



# import object as o
# billard = o.Pool(1)
#update_pool(billard,10)
#print(billard)

'''queue = o.Cue(1)
queue.frappe(1,0,billard.balls["0"])
update_pool(billard,52)
print(billard)'''

def distance(ball1,ball2):
    position_vector1 = ball1.position
    position_vector2 = ball2.position
    return np.sqrt((position_vector1[0]-position_vector2[0])**2+(position_vector1[1]-position_vector2[1])**2)

def norm(vector):
    return np.sqrt(vector[0]**2+vector[1]**2)

def collided(ball1,ball2):
    return distance(ball1,ball2) < ball1.radius + ball2.radius

def packed(ball1,ball2,epsilon):
    return distance(ball1,ball2) < ball1.radius + ball2.radius + epsilon

def collision_matrix(balls,number_of_balls):
    # le deuxieme argument correspond au nombre de boules
    matrix = np.zerros((number_of_balls,number_of_balls))
    for i in range(number_of_balls):
        for j in range(number_of_balls-i):
            matrix[i][j] = collided(balls[str(i)],balls[str(j)])
            matrix[j][i] = matrix[i][j]
    return matrix

def orientation_vector(ball1,ball2):
    vector = ball1.position - ball2.position
    return vector/norm(vector)


class Packed_balls():
    def __init__(self,balls,number_of_balls,epsilon):
        self.balls = balls
        self.packs = self.get_packs(epsilon) # np matrix
        self.number_of_balls = number_of_balls
        self.admission_vector = self.get_admission_vector()

    def get_packs(self,epsilon):
        number_of_balls = self.number_of_balls
        balls = self.balls
        matrix = np.zerros((number_of_balls,number_of_balls))
        for i in range(number_of_balls):
            for j in range(number_of_balls-i):
                matrix[i][j] = packed(balls[str(i)],balls[str(j)],epsilon)
                matrix[j][i] = matrix[i][j]
        return matrix

    def get_admission_vector(self):
        number_of_balls = self.number_of_balls
        balls = self.balls
        packs = self.packs
        vectors = {}
        for i in range(number_of_balls):
            vector_i = np.array([0,0])
            for j in range(number_of_balls):
                if i==j:
                    vector_i += np.array([0,0])
                else:
                    vector_i += orientation_vector(balls[str(i)],balls[str(j)])
            vectors[str(i)] = vector_i / norm(vector_i)
        return vectors
    

    
