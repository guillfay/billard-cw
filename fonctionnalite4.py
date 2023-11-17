import numpy as np


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


# script de test
"""from objet import *
dt = 0.001 #pas de temps
Board = Board()
Ball = Ball(1, np.array([0.003, 0.003])) #position initial proche du coin en bas à gauche

bounce_status = detect(Board, Ball, dt)
print(Ball)
print(bounce_status)

print("### update speed ###")
Ball.update_speed(np.array([-1,-2]))
bounce_status = detect(Board, Ball, dt)
print(Ball)
print(bounce_status)
print(rebond(Board, Ball, dt, bounce_status))"""
