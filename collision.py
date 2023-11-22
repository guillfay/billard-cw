import objet as objet
import dynamic as dynamic
import numpy as np
import copy 
import matplotlib.pyplot as plt

def update_pool(pool,delta_t):
    #version sans interactions entre les boules et sans frottements
    number_of_balls = pool.number_of_balls
    balls = pool.balls
    width = pool.board.corners[3][0]
    length = pool.board.corners[3][1]
    virtual_position_matrix = np.zerros(number_of_balls)
    for ball in balls.values():
        virtual_position = ball.position + delta_t*ball.speed 
        
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

def scalar_product(vector1,vector2):
    return vector1[0]*vector2[0] + vector1[1]*vector2[1]

def scalar(vec1, vec2):
    return np.dot(vec1, vec2)

def norme(vec):
    return np.sqrt(vec[0]**2 + vec[1]**2)

def vecmiddle(vec1, vec2):
    vec = np.sum(vec1, vec2)
    N = norme(vec)
    return np.array([vec[0]/N, vec[1]/N])

def collided(ball1,ball2):
    if distance(ball1,ball2) < ball1.radius + ball2.radius : 
        return True
    else :
        return False

def packed(ball1,ball2,epsilon):
    if distance(ball1,ball2) <= ball1.radius + ball2.radius + epsilon : #le egal est tres important pour update_pool
        return True 
    else :
        return False
    
def collision_matrix(pool):
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    # le deuxieme argument correspond au nombre de boules
    matrix = np.zeros((number_of_balls,number_of_balls))
    for i in range(number_of_balls):
        for j in range(i+1,number_of_balls):
            matrix[i][j] = collided(balls[i],balls[j])
            matrix[j][i] = matrix[i][j]
        matrix[i][i] = 0
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
        self.neighbors = self.get_neighbors()

    def get_packs(self,epsilon):
        number_of_balls = self.number_of_balls
        balls = self.balls
        matrix = np.zeros((number_of_balls,number_of_balls))
        for i in range(number_of_balls):
            for j in range(i,number_of_balls):
                matrix[i][j] = packed(balls[i],balls[j],epsilon)
                matrix[j][i] = matrix[i][j]
            matrix[i][i] = 0
        return matrix>0

    def get_admission_vector(self):
        number_of_balls = self.number_of_balls
        balls = self.balls
        packs = self.packs
        vectors = {}
        for i in range(number_of_balls):
            vector_i = np.array([0,0])
            #print(vector_i)
            for j in range(number_of_balls):
                if self.packs[i][j] and i!=j:
                    #print(orientation_vector(balls[i],balls[j]))
                    vector_i = vector_i + orientation_vector(balls[j],balls[i])
            if norm(vector_i)!=0 :
                vectors[i] = vector_i / norm(vector_i)
            else :
                vectors[i] = vector_i
        return vectors
    
    def get_neighbors(self):
        packs = self.packs
        number_of_balls = self.number_of_balls
        neighbors = {i : 0 for i in range(number_of_balls)}
        for i in range(number_of_balls):
            for j in range(i+1,number_of_balls):
                if packs[i][j]:
                    neighbors[i] += 1
                    neighbors[j] += 1
        return neighbors

def impact_time(ball1,ball2,epsilon):
    square_radius = (ball1.radius+ball2.radius+epsilon)**2
    Delta_Vx = ball2.speed[0] - ball1.speed[0]
    Delta_Vy = ball2.speed[1] - ball1.speed[1]
    Delta_X =  ball2.position[0] - ball1.position[0]
    Delta_Y =  ball2.position[1] - ball1.position[1]
    a = Delta_Vx**2 + Delta_Vy**2
    b = 2*Delta_X*Delta_Vx + 2*Delta_Y*Delta_Vy
    c = Delta_X**2 + Delta_Y**2 - square_radius
    if a == 0 :
        sol1 = -c/b
        sol2 = sol1
    else :
        Delta = b**2 - 4*a*c
        sqrt_delta = np.sqrt(Delta)
        sol1 = (-b+sqrt_delta)/(2*a)
        sol2 = (-b-sqrt_delta)/(2*a)
    sol1 = max(0,sol1)
    sol2 = max(0,sol2) 
    return min(sol1,sol2) #on garde la plus petite solution positive

def first_impact(pool,potential_collisions,epsilon):
    number_of_balls = pool.number_of_balls
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

    return np.min(matrix),index

def update_position(pool,delta_t):
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        new_position = pool.balls[i].position + delta_t*pool.balls[i].speed
        pool.balls[i].update_speed(pool.balls[i].speed)
        pool.balls[i].update_position(new_position)

def collision_update_speed(pool,number_of_balls,packs):
    #conservation de la quantité de mouvement
    #redistribution de p parmis les packs
    balls = pool.balls
    initial_speed = np.array([balls[i].speed for i in range(number_of_balls)]) 
    exchanged_speed = np.zeros((number_of_balls, 2))
    rebound_speed = np.zeros((number_of_balls, 2))
    final_speed = np.zeros((number_of_balls, 2))
    for i in range(number_of_balls):
        received_speed_i = np.array([0,0])
        for j in range(number_of_balls):
            if packs.packs[i][j] :
                p_j = balls[j].mass * initial_speed[j]
                u_ji = orientation_vector(balls[i],balls[j])
                received_speed_i = received_speed_i + (1-scalar_product(p_j,u_ji))/(balls[i].mass*packs.neighbors[j])*u_ji
                exchanged_speed[i] = exchanged_speed[i] + received_speed_i
        p_i = balls[i].mass * initial_speed[i]
        u_i = packs.admission_vector[i]
        rebound_speed[i] = scalar_product(u_i,p_i)/(balls[i].mass)*u_i
    for i in range(number_of_balls):
        final_speed[i] = initial_speed[i]+exchanged_speed[i]+rebound_speed[i]
        balls[i].update_speed(final_speed[1])
      
def lst_balls_impacted_by_ref(num_ball_ref, dicoimpact, dicoballs):
    lst = []
    lst_balls_touching_ref = dicoimpact[num_ball_ref]
    ballref = dicoballs[num_ball_ref]
    for num_ball_touching_ref in lst_balls_touching_ref :
        ball_touching_ref = dicoballs[num_ball_touching_ref]
        vref_scalar_v = scalar(ballref.speed, ball_touching_ref.position - ballref.position)
        if vref_scalar_v >= 0:
            lst.append(num_ball_touching_ref)
    return lst

def update_speed_collision(pool,number_of_balls, packs):
    pack = packs.packs
    dicoballs = pool.balls
    n = number_of_balls
    dicoimpact = {} 
    for i in range(n) : # moyen d'augmenter la rapidité ici si pb
        check = dicoimpact.get(i, False)
        for j in range(n):
            if pack[i][j]:
                if not check : 
                    dicoimpact[i] = [j]
                else :
                    dicoimpact[i].append(j)
    dicoimpact_by_ref = {}
    dico_dv = {}
    for i in range(n):
        dico_dv[i] = 0
    for num_ball_ref in dicoimpact:
        ballref = dicoballs[num_ball_ref]
        lst = lst_balls_impacted_by_ref(num_ball_ref, dicoimpact, dicoballs)
        dicoimpact_by_ref[num_ball_ref] = lst
        if len(lst) == 1:
            num_ball_impacted1 = lst[0]
            ballimpacted1 = dicoballs[num_ball_impacted1]
            vec_refto1 = ballimpacted1.position - ballref.position
            vec_refto1 = vec_refto1 / norme(vec_refto1)
            dvimpacted1 = scalar(ballref.speed, vec_refto1) * vec_refto1
            dvref = - dvimpacted1
            dico_dv[num_ball_impacted1] += dvimpacted1
            dico_dv[num_ball_ref] += dvref
        elif len(lst) == 2:
            num_ball_impacted1 = lst[0]
            num_ball_impacted2 = lst[1]
            ballimpacted1 = dicoballs[num_ball_impacted1]
            ballimpacted2 = dicoballs[num_ball_impacted2]
            vec_refto1 = ballimpacted1.position - ballref.position
            vec_refto1 = vec_refto1 / norme(vec_refto1)
            vec_refto2 = ballimpacted2.position - ballref.position
            vec_refto2 = vec_refto2 / norme(vec_refto2)
            vec_reftomiddle12 = vecmiddle(vec_refto1, vec_refto2)
            l = scalar(vec_refto1, vec_reftomiddle12)
            h = scalar(ballref.speed, vec_reftomiddle12) #voir schéma pour comprendre
            rsquare = (h**2) * (1-l**2) / (l**2)
            n1 = np.sqrt(rsquare + (h**2))
            n2 = n1
            dvimpacted1 = n1 * vec_refto1
            dvimpacted2 = n2 * vec_refto2
            dvref = - h
            scalar1 = scalar(ballref.speed + dvref, vec_refto1)
            scalar2 = scalar(ballref.speed + dvref, vec_refto2)
            if scalar1 >= 0:
                dvimpacted1 += scalar1 * vec_refto1
                dvref += - dvimpacted1
            elif scalar2 >= 0:
                dvimpacted2 += scalar2 * vec_refto2
                dvref += - dvimpacted2
            dico_dv[num_ball_impacted1] += dvimpacted1
            dico_dv[num_ball_impacted2] += dvimpacted2
            dico_dv[num_ball_ref] += dvref
        elif len(lst) == 3:
            num_ball_impacted1 = lst[0]
            num_ball_impacted2 = lst[1]
            num_ball_impacted3 = lst[2]
            ballimpacted1 = dicoballs[num_ball_impacted1]
            ballimpacted2 = dicoballs[num_ball_impacted2]
            ballimpacted3 = dicoballs[num_ball_impacted3]
            vec_refto1 = ballimpacted1.position - ballref.position
            vec_refto1 = vec_refto1 / norme(vec_refto1)
            vec_refto2 = ballimpacted2.position - ballref.position
            vec_refto2 = vec_refto2 / norme(vec_refto2)
            vec_refto3 = ballimpacted3.position - ballref.position
            vec_refto3 = vec_refto3 / norme(vec_refto3)
        
        #jusqu'ici tout roule normalement mais pour le reste du cas ou la boule de reference touche 3 boules en même temps je seche complet...
        
            """vec_reftomiddle12 = vecmiddle(vec_refto1, vec_refto2)
            vec_reftomiddle12 = vecmiddle(vec_refto1, vec_refto2)
            l = scalar(vec_refto1, vec_reftomiddle12)
            h = scalar(ballref.speed, vec_reftomiddle12)
            rsquare = (h**2) * (1-l**2) / (l**2)
            n1 = np.sqrt(rsquare + (h**2))
            n2 = n1
            dvimpacted1 = n1 * vec_refto1
            dvimpacted2 = n2 * vec_refto2
            dvref = - h
            scalar1 = scalar(ballref.speed + dvref, vec_refto1)
            scalar2 = scalar(ballref.speed + dvref, vec_refto2)
            if scalar1 >= 0:
                dvimpacted1 += scalar1 * vec_refto1
                dvref += - dvimpacted1
            elif scalar2 >= 0:
                dvimpacted2 += scalar2 * vec_refto2
                dvref += - dvimpacted2
            dico_dv[num_ball_impacted1] += dvimpacted1
            dico_dv[num_ball_impacted2] += dvimpacted2
            dico_dv[num_ball_ref] += dvref"""

    for num_ball in dico_dv :
        ball = dicoballs[num_ball]
        ball.speed = ball.speed + dico_dv[num_ball]

def update_balls_bounce(board, ball, dt, bounce_status):
    new_pos = ball.position + ball.speed * dt
    new_speed = ball.speed

    x_min = min([corner[0] for corner in board.corners]) + ball.radius
    x_max = max([corner[0] for corner in board.corners]) - ball.radius
    y_min = min([corner[1] for corner in board.corners]) + ball.radius
    y_max = max([corner[1] for corner in board.corners]) - ball.radius
    
    def rebond_x(x_bord, x_virt):
        return 2 * x_bord - x_virt

    def rebond_y(y_bord, y_virt):
        return 2 * y_bord - y_virt

    if bounce_status[0]:
        new_pos[0] = rebond_x(x_min, new_pos[0])
        new_speed = new_speed * np.array([-1, 1])
    if bounce_status[2]:
        new_pos[0] = rebond_x(x_max, new_pos[0])
        new_speed = new_speed * np.array([-1, 1])
    if bounce_status[3]:
        new_pos[1] = rebond_y(y_min, new_pos[1])
        new_speed = new_speed * np.array([1, -1])
    if bounce_status[1]:
        new_pos[1] = rebond_y(y_max, new_pos[1])
        new_speed = new_speed * np.array([1, -1])

    return new_pos, new_speed

def detect(board, ball, dt):
    """Cette fonction prend en argument une table, une balle et l'incrément de temps.
    Elle calcule la position de la boule après dt, et renvoie un tuple indiquant s'il y a un ou des rebonds sur les
    bandes. L'ordre du tuple part du bord de gauche, en x=0, et tourne dans le sens horaire"""

    pos_virt = ball.position + ball.speed * dt

    x_min = min([corner[0] for corner in board.corners]) + ball.radius
    x_max = max([corner[0] for corner in board.corners]) - ball.radius
    y_min = min([corner[1] for corner in board.corners]) + ball.radius
    y_max = max([corner[1] for corner in board.corners]) - ball.radius

    return pos_virt[0] < x_min, pos_virt[1] > y_max, pos_virt[0] > x_max, pos_virt[1] < y_min

# def update_speed_2collidedBalls5(pool,index):
#     deltaV_1 = 0
#     deltaV_0 = 0
#     v_0 = pool.balls[index[0]].speed
#     v_1 = pool.balls[index[1]].speed
#     u_0to1 = ball1.position-ball0.position
#     u_0to1 = u_0to1 / norm(u_0to1)
#     print(u_0to1)
#     u_0to1_T = np.array([-u_0to1[1],u_0to1[0]])
#     deltaV_1 = np.dot(v_0, u_0to1) * u_0to1
#     deltaV_0 = -np.dot(v_0, u_0to1_T) * u_0to1_T
#     u_1to0 = -u_0to1
#     u_1to0_T = -u_0to1_T
#     deltaV_0 += np.dot(v_1, u_1to0) * u_1to0
#     deltaV_1 += -np.dot(v_1, u_1to0_T) * u_1to0_T
#     new_speed0 = deltaV_0
#     new_speed1 = deltaV_1
#     pool.balls[index[0]].update_speed(new_speed0)
#     pool.balls[index[1]].update_speed(new_speed1)

def update_speed_2collidedBalls(pool,index):
    ball1 = pool.balls[index[0]]
    ball2 = pool.balls[index[1]]
    vec_1to2 = ball2.position - ball1.position
    vec_1to2 = vec_1to2 / norm(vec_1to2)
    deltaV = scalar_product(ball1.speed+ball2.speed, vec_1to2)
    if deltaV >= 0:
        deltaV_2 = np.sqrt(norme(ball1.speed) **2 + norme(ball2.speed) **2 - norme(ball1.speed - scalar_product(ball1.speed, vec_1to2) * vec_1to2) **2 - norme(ball2.speed - scalar_product(ball2.speed, vec_1to2) * vec_1to2) **2) * vec_1to2 - scalar_product(ball2.speed, vec_1to2) * vec_1to2
        deltaV_1 = - scalar_product(ball1.speed, vec_1to2) * vec_1to2
    else:
        deltaV_1 = np.sqrt(norme(ball1.speed) **2 + norme(ball2.speed) **2 - norme(ball1.speed - scalar_product(ball1.speed, vec_1to2) * vec_1to2) **2 - norme(ball2.speed - scalar_product(ball2.speed, vec_1to2) * vec_1to2) **2) * (-vec_1to2) - scalar_product(ball1.speed, vec_1to2) * vec_1to2
        deltaV_2 = - scalar_product(ball2.speed, vec_1to2) * vec_1to2
    new_speed1 = ball1.speed + deltaV_1
    new_speed2 = ball2.speed + deltaV_2
    pool.balls[index[0]].update_speed(new_speed1)
    pool.balls[index[1]].update_speed(new_speed2)

def detection_of_collision(potential_collisions,number_of_balls):
    for i in range(number_of_balls):
        for j in range(i+1,number_of_balls):
            if potential_collisions[i][j] :
                return True
    return False

def friction(pool,delta_t,alpha=0.95,v_min=0.01):
    balls = pool.balls 
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        if norm(balls[i].speed) < v_min :
            balls[i].update_speed(np.array([0,0]))
        else :
            deltaV = delta_t*alpha*balls[i].speed/norm(balls[i].speed)
            new_speed = balls[i].speed - deltaV
            balls[i].update_speed(new_speed)

def at_equilibrium(pool):
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        if norm(balls[i].speed)>0 :
            return False
    return True

def bounce(pool,delta_t):
    balls = pool.balls
    for ball in balls.values():
                bounce_status = detect(pool.board, ball, delta_t)
                new_pos, new_speed = update_balls_bounce(pool.board, ball, delta_t, bounce_status)
                if pool.type_billard!='francais':
                    check_exit(pool,ball)
                update_ball(ball,new_pos,new_speed)ball.update_position(new_pos)
                ball.update_speed(new_speed)

def update_real_pool(pool,delta_t,epsilon = 0.01):
    # iteration naïve sans interactions physiques
    naive_pool = copy.deepcopy(pool)
    update_position(naive_pool,delta_t) #on update les boules sans chocs pour voir si elles se superposent
    # detection de chocs
    potential_collisions = collision_matrix(naive_pool)
    if np.any(potential_collisions):
    #if detection_of_collision(potential_collisions,number_of_balls): #Verifie qu'il y a un True dans la matrice
        t_0, collided_balls = first_impact(pool,potential_collisions,epsilon) #on extrait le moment du premier choc
        if t_0 < delta_t:
            update_position(pool,t_0) #on update les boules au moments du premier choc
            update_speed_2collidedBalls(pool,collided_balls)
            bounce(pool,delta_t)
            if t_0 != 0 :
                update_real_pool(pool,delta_t-t_0,epsilon)
        #print(np.sum([np.linalg.norm(balls[i].speed)**2 for i in range(number_of_balls)]))

        update_position(pool,delta_t)
        #friction(pool,delta_t,alpha=0.1,v_min=0.01)
        friction(pool,delta_t,alpha=30,v_min=0.05)
        bounce(pool,delta_t)
    else :
        bounce(pool,delta_t)
        friction(pool,delta_t,alpha=30,v_min=0.05)
    return at_equilibrium(pool)

def check_exit(pool,ball):
    pos=ball.position
    pockets=Board.get_pockets(pool.board)
    for j in range(len(pockets)):
        if linalg.norm(pos-pockets[j])<2*ball.radius:
            ball.update_state(False)

def update_ball(ball,new_pos,new_speed):
    if ball.state==False:
        ball.update_position(np.array([-10*ball.position[0],-10*ball.position[1]]))
        ball.update_speed(np.array([0,0]))
        print("FIN DE PARTIE")
    else:
        ball.update_position(new_pos)
        ball.update_speed(new_speed)



    #s'il n'y a pas de chocs on regarde s'il y a des rebonds
    #fin de l'itération on fait les frottements
    # if rebond :

##################################################################### TEST #################

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


billard2 = objet.Pool(3)
billard2.board.set_size(15,15)
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
ball2 = billard2.balls[2]
for i in range(3):
    billard2.balls[i].update_position(np.array([4*i+1,1]))
billard2.balls[0].update_speed(np.array([1,0]))
#billard2.balls[2].update_speed(np.array([-1,0]))

time_list = np.array([])
x_list = np.array([])
for i in range(500):
    time_list = np.append(time_list,i*0.5)
    x_list = np.append(x_list,billard2.balls[1].position[0])
    update_real_pool(billard2,0.5)

plt.plot(time_list, x_list, label='Position en X')
plt.xlabel('Temps')
plt.ylabel('Position en X')
plt.title('Évolution de la position en X en fonction du temps')
plt.legend()
plt.show()


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

