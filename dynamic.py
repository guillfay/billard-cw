import numpy as np
from objet_game import *

def update_pool(pool, delta_t):
    # version initiale sans rebond et sans interactions entre les boules et sans frottements
    balls = pool.balls
    for ball in balls.values():
        bounce_status = detect(pool.board, ball, delta_t)
        new_pos, new_speed = rebond(pool.board, ball, delta_t, bounce_status)
        if pool.type_billard!='francais':
            check_exit(pool,ball)
        update_ball(ball,new_pos,new_speed)
    
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
        print()
    else:
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

# from objet import *
# from graphique import *
# from functools import partial

# my_pool = Pool(2)
# cue = Cue(0.5)
# cue.frappe(0.5, np.pi/3, my_pool.balls[0])

# animation = trace(my_pool, partial(update_pool, pool=my_pool, deltaT=1/60))
# plt.show()
