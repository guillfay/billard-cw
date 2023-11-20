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

def distance(ball1,ball2):
    position_vector1 = ball1.position
    position_vector2 = ball2.position
    return np.sqrt((position_vector1[0]-position_vector2[0])**2+(position_vector1[1]-position_vector2[1])**2)

def norm(vector):
    return np.sqrt(vector[0]**2+vector[1]**2)

def collided(ball1,ball2):
    if distance(ball1,ball2) < ball1.radius + ball2.radius : 
        print(ball1.radius + ball2.radius)
        return True
    else :
        return False

def packed(ball1,ball2,epsilon):
    if distance(ball1,ball2) < ball1.radius + ball2.radius + epsilon : 
        return True
    else :
        return False
    
def collision_matrix(balls,number_of_balls):
    # le deuxieme argument correspond au nombre de boules
    matrix = np.zeros((number_of_balls,number_of_balls))
    for i in range(number_of_balls):
        for j in range(i,number_of_balls):
            matrix[i][j] = collided(balls[i],balls[j])
            print("testetstetstet", matrix[i][j])
            matrix[j][i] = matrix[i][j]
    return matrix>0

def orientation_vector(ball1,ball2):
    vector = ball1.position - ball2.position
    return np.array(vector/norm(vector))


class Packed_balls():
    def __init__(self,balls,number_of_balls,epsilon):
        self.balls = balls
        self.number_of_balls = number_of_balls
        self.packs = self.get_packs(epsilon) # np matrix
        self.admission_vector = self.get_admission_vector()

    def get_packs(self,epsilon):
        number_of_balls = self.number_of_balls
        balls = self.balls
        matrix = np.zeros((number_of_balls,number_of_balls))
        for i in range(number_of_balls):
            for j in range(i,number_of_balls):
                matrix[i][j] = packed(balls[i],balls[j],epsilon)
                matrix[j][i] = matrix[i][j]
        return matrix>0

    def get_admission_vector(self):
        number_of_balls = self.number_of_balls
        balls = self.balls
        packs = self.packs
        vectors = {}
        for i in range(number_of_balls):
            vector_i = np.zeros(2)
            #print(vector_i)
            for j in range(number_of_balls):
                if i==j:
                    vector_i += np.array([0,0])
                else:
                    #print(orientation_vector(balls[i],balls[j]))
                    vector_i += orientation_vector(balls[i],balls[j])
            vectors[str(i)] = vector_i / norm(vector_i)
        return vectors

def impact_time(ball1,ball2,epsilon):
    square_radius = (ball1.radius+ball2.radius+epsilon)**2
    Delta_Vx = ball2.speed[0] - ball1.speed[0]
    Delta_Vy = ball2.speed[1] - ball1.speed[1]
    Delta_X =  ball2.position[0] - ball1.position[0]
    Delta_Y =  ball2.position[1] - ball1.position[1]
    a = Delta_Vx**2 + Delta_Vy**2
    b = 2*Delta_X*Delta_Vx + 2*Delta_Y*Delta_Vy
    c = Delta_X + Delta_Y - square_radius
    Delta = b**2 - 4*a*c
    sqrt_delta = np.sqrt(Delta)
    if a == 0 :
        sol1 = -c/b
        sol2 = sol1
    else :
        sol1 = (b+sqrt_delta)/(2*a)
        sol2 = (b-sqrt_delta)/(2*a)
    sol1 = max(0,sol1)
    sol2 = max(0,sol1)
    return min(sol1,sol2)

def detection_of_collision(potential_collisions,number_of_balls):
    for i in range(number_of_balls):
        for j in range(i+1,number_of_balls):
            if potential_collisions[i][j] :
                return True
    return False

def collision_update_speed():
    pass

def first_impact_time(pool,potential_collisions,number_of_balls,epsilon):
    matrix = np.zeros((number_of_balls,number_of_balls))
    for i in range(number_of_balls):
        matrix[i][i] = np.inf
        for j in range(i+1,number_of_balls):
            if potential_collisions[i][j]:
                matrix[i][j] = impact_time(pool.balls[i],pool.balls[j],epsilon)
            else :
                matrix[i][j] = np.inf
            matrix[j][i] = matrix[i][j]
    index = np.array(np.unravel_index(np.argmin(matrix), matrix.shape))
    return matrix[index[0]][index[1]]

def update_real_pool(pool,deltaT,epsilon = 0.01):
    #version sans frottements
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    width = pool.board.corners[3][0]
    length = pool.board.corners[3][1]
    # iteration naïve sans interactions physiques
    naive_pool = objet.Pool(number_of_balls)
    for i in range(number_of_balls):
        virtual_position = pool.balls[i].position + deltaT*pool.balls[i].speed
        naive_pool.balls[i].update_speed(pool.balls[i].speed)
        naive_pool.balls[i].update_position(virtual_position)
    # detection de chocs
    potential_collisions = collision_matrix(naive_pool.balls,number_of_balls)
    if detection_of_collision(potential_collisions,number_of_balls): 
        t_0 = first_impact_time(pool,potential_collisions,number_of_balls,epsilon) #on extrait le moment du premier choc


    #s'il n'y a pas de chocs on regarde s'il y a des rebonds
    # if rebond :
    print("le billard naif", naive_pool)
    print("il y a des collisions",detection_of_collision(potential_collisions,number_of_balls))



'''billard = objet.Pool(8)
print(billard)
ball1 = billard.balls[1]
ball2 = billard.balls[2]
ball3 = billard.balls[3]

#test de distance, pour deux boules au meme endroit
print("test de distance", distance(ball1,ball2))

#test de distance, pour deux boules decallés de 1
new_position = ball1.position - np.array([1,0])
ball1.update_position(new_position)
print("test de distance", distance(ball1,ball2))

#test de norm
vector = np.array([1,0])
print("test de norm", norm(vector))

#test de collided
print("test de collided", collided(ball1,ball2))
print("test de collided", collided(ball3,ball2))

#toutes les boules sont en chocs sauf la deux, qui est logiquement en choc avec elle meme
print(collision_matrix(billard.balls,8))

#test de collision vector de 2 vers 1
print(orientation_vector(ball1,ball2))

#paquets = Packed_balls(billard.balls,8,0.1)
'''

billard2 = objet.Pool(3)
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
ball2 = billard2.balls[2]
for i in range(3):
    billard2.balls[i].update_position(np.array([3*i,0]))
billard2.balls[0].update_speed(np.array([1,0]))
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
ball2 = billard2.balls[2]
update_real_pool(billard2,1.1)
'''
new_position = ball1.position - np.array([1,0])
billard2.balls[1].update_position(new_position)
new_speed = ball1.speed - np.array([1,0])
billard2.balls[1].update_speed(new_speed)
print(billard2)
paquets = Packed_balls(billard2.balls,2,0.1)

print(ball1.radius+ball0.radius)
print(paquets.packs)
ball1.update_position(new_position)
print(paquets.admission_vector)
print(impact_time(ball1,ball0,0.001))

print(billard2.number_of_balls)
billard2.balls[1].update_speed(np.array([1,0]))
update_real_pool(billard2,0.99)'''
