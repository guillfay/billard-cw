import objet as objet
import dynamic as dynamic
import numpy as np
import copy 

def collided(ball1,ball2): 
    '''Vérifie si les deux boules se superposent, i.e : s'entrechoquent'''
    if np.linalg.norm(ball1.position-ball2.position) < ball1.radius + ball2.radius : 
        return True
    else :
        return False
   
def collision_matrix(pool): 
    '''Crée une matrice de booléen telle que matrix[i][j]
    #est True si les boules i et j s'entrechoquent
    False sinon'''
    balls = pool.balls
    for ball in balls.values():
        bounce_status = detect(pool.board, ball, delta_t)
        new_pos, new_speed = rebond(pool.board, ball, delta_t, bounce_status)
        ball.update_position(new_pos)
        ball.update_speed(new_speed)


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

def update_speed_2collidedBalls(pool,index):
    '''Met à jour la vitesse de deux boules qui s'entrechoquent'''
    ball1 = pool.balls[index[0]]
    ball2 = pool.balls[index[1]]
    vec_1to2 = ball2.position - ball1.position
    vec_1to2 = vec_1to2 / np.linalg.norm(vec_1to2)
    deltaV = np.dot(ball1.speed+ball2.speed, vec_1to2)
    v1 = ball1.speed
    v1n = np.dot(ball1.speed, vec_1to2) * vec_1to2
    v1t = ball1.speed - v1n
    v2 = ball2.speed
    v2n = np.dot(ball2.speed, vec_1to2) * vec_1to2
    v2t = ball2.speed - v2n
    if deltaV >= 0:
        deltaV_2 = np.sqrt(np.linalg.norm(v1)**2 + np.linalg.norm(v2)**2 - np.linalg.norm(v1t)**2 - np.linalg.norm(v2t)**2) * vec_1to2 - v2n
        deltaV_1 = - v1n
    else:
        deltaV_1 = np.sqrt(np.linalg.norm(v1)**2 + np.linalg.norm(v2)**2 - np.linalg.norm(v1t)**2 - np.linalg.norm(v2t)**2) * (-vec_1to2) - v1n
        deltaV_2 = - v2n
    new_speed1 = ball1.speed + deltaV_1
    new_speed2 = ball2.speed + deltaV_2
    pool.balls[index[0]].update_speed(new_speed1)
    pool.balls[index[1]].update_speed(new_speed2)

def friction(pool,delta_t,alpha=0.95,v_min=0.01):
    '''Met à jour la vitesse de toutes les boules de sorte que toutes les secondes 
    elles perdent alpha (en pourcentage) de leur vitesse. De plus,
    elle arrête les boules qui ont une vitesse inférieure en norme a v_min'''

    balls = pool.balls 
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        if np.linalg.norm(balls[i].speed) < v_min :
            balls[i].update_speed(np.array([0,0]))
        else :
            deltaV = delta_t*alpha*balls[i].speed/np.linalg.norm(balls[i].speed)
            new_speed = balls[i].speed - deltaV
            balls[i].update_speed(new_speed)

def at_equilibrium(pool):
    '''Renvoie True si toutes les boules sont à l'arrêt, False sinon.'''
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    for i in range(number_of_balls):
        if np.linalg.norm(balls[i].speed)>0 :
            return False
    return True

def bounce(pool,delta_t):
    '''Mets à jour la position et la vitesse de toutes les boules si celles-ci
    ont rebondi contre un bord '''
    balls = pool.balls
    for ball in balls.values():
                bounce_status = detect(pool.board, ball, delta_t)
                new_pos, new_speed = update_balls_bounce(pool.board, ball, delta_t, bounce_status)
                ball.update_position(new_pos)
                ball.update_speed(new_speed)

def update_pool(pool,delta_t,epsilon = 0.1):
    # iteration naïve sans interactions physiques
    naive_pool = copy.deepcopy(pool)
    update_position(naive_pool,delta_t) #on update les boules sans chocs pour voir si elles se superposent
    # Detection des chocs
    potential_collisions = collision_matrix(naive_pool)
    if np.any(potential_collisions):
        t_0, collided_balls = first_impact(pool,potential_collisions,epsilon) #on extrait le moment du premier choc
        if t_0 < delta_t:
            update_position(pool,t_0) #on update les boules au moments du premier choc
            update_speed_2collidedBalls(pool,collided_balls)
            bounce(pool,delta_t)
            if t_0 != 0 :
                update_pool(pool,delta_t-t_0,epsilon)

        '''test de conservation de l'energie cinétique : '''
        #print(np.sum([np.linalg.norm(balls[i].speed)**2 for i in range(number_of_balls)]))

        update_position(pool,delta_t)
        friction(pool,delta_t,alpha=0.3,v_min=0.05)
        bounce(pool,delta_t)
    else :
        bounce(pool,delta_t)
        friction(pool,delta_t,alpha=0.3,v_min=0.05)
    return at_equilibrium(pool)
