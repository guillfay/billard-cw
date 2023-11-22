import numpy as np


def update_pool(pool, delta_t):
    # version initiale sans rebond et sans interactions entre les boules et sans frottements
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


def rebond(board, ball, dt, bounce_status):
    pos_reel = ball.position + ball.speed * dt
    speed_reel = ball.speed

    x_min = min([corner[0] for corner in board.corners]) + ball.radius
    x_max = max([corner[0] for corner in board.corners]) - ball.radius
    y_min = min([corner[1] for corner in board.corners]) + ball.radius
    y_max = max([corner[1] for corner in board.corners]) - ball.radius

    def rebond_x(x_bord, x_virt):
        return 2 * x_bord - x_virt

    def rebond_y(y_bord, y_virt):
        return 2 * y_bord - y_virt

    if bounce_status[0]:
        pos_reel[0] = rebond_x(x_min, pos_reel[0])
        speed_reel = speed_reel * np.array([-1, 1])
    if bounce_status[2]:
        pos_reel[0] = rebond_x(x_max, pos_reel[0])
        speed_reel = speed_reel * np.array([-1, 1])

    if bounce_status[3]:
        pos_reel[1] = rebond_y(y_min, pos_reel[1])
        speed_reel = speed_reel * np.array([1, -1])
    if bounce_status[1]:
        pos_reel[1] = rebond_y(y_max, pos_reel[1])
        speed_reel = speed_reel * np.array([1, -1])

    return pos_reel, speed_reel

def distance(ball1,ball2):
    position_vector1 = ball1.position
    position_vector2 = ball2.position
    return np.sqrt((position_vector1[0]-position_vector2[0])**2+(position_vector1[1]-position_vector2[1])**2)

def norm(vector):
    return np.sqrt(vector[0]**2+vector[1]**2)

def scalar_product(vector1,vector2):
    return vector1[0]*vector2[0] + vector1[1]*vector1[1]

def collided(ball1,ball2):
    if distance(ball1,ball2) < ball1.radius + ball2.radius : 
        return True
    else :
        return False

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

def collision_matrix(balls,number_of_balls):
    # le deuxieme argument correspond au nombre de boules
    matrix = np.zeros((number_of_balls,number_of_balls))
    for i in range(number_of_balls):
        for j in range(i,number_of_balls):
            matrix[i][j] = collided(balls[i],balls[j])
            matrix[j][i] = matrix[i][j]
    return matrix>0


# my_pool = Pool(2)
# cue = Cue(0.5)
# cue.frappe(0.5, np.pi/3, my_pool.balls[0])

# animation = trace(my_pool, partial(update_pool, pool=my_pool, deltaT=1/60))
# plt.show()
