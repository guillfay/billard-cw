import numpy as np

def detect(board, ball, dt):
    x = ball.position[0]
    y = ball.position[1]
    vx = ball.speed[0]
    vy = ball.speed[1]
    xp = x + vx*dt
    yp = y + vy*dt
    r = ball.radius
    ylignbetween12 = board.corners[0][1] + r
    xlignbetween23 = board.corners[1][0] - r
    ylignbetween34 = board.corners[2][1] - r
    xlignbetween41 = board.corners[3][0] + r
    if yp < ylignbetween12 and xlignbetween41 < xp < xlignbetween23:
        return 1
    elif xp > xlignbetween23 and ylignbetween12 < yp < ylignbetween34:
        return 2
    elif yp > ylignbetween34 and xlignbetween41 < xp < xlignbetween23:
        return 3
    elif xp < xlignbetween41 and ylignbetween12 < yp < ylignbetween34:
        return 4
    elif xlignbetween41 < xp < xlignbetween23 and ylignbetween12 < yp < ylignbetween34:
        return 0
    else: #ici c'est pour gagner du temps de calcul je me dis que c'est assez rare quand meme d'avoir 2 rebonds
        if yp < ylignbetween12 and xp < xlignbetween41:
            return 11
        elif yp < ylignbetween12 and xp > xlignbetween23:
            return 22
        if yp > ylignbetween34 and xp > xlignbetween23:
            return 33
        elif yp > ylignbetween34 and xp < xlignbetween41:
            return 44
        

def rebond(board, ball, dt):
    x = ball.position[0]
    y = ball.position[1]
    vx = ball.speed[0]
    vy = ball.speed[1]
    r = ball.radius
    ylignbetween12 = board.corners[0][1] + r
    xlignbetween23 = board.corners[1][0] - r
    ylignbetween34 = board.corners[2][1] - r
    xlignbetween41 = board.corners[3][0] + r
    check = detect(board, ball, dt)
    if check == 1:
        speedafter = np.array([vx, -vy])
        posafter = np.array([x + vx*dt, -(y + vy*dt) + 2*ylignbetween12])
    elif check == 2:
        speedafter = np.array([-vx, vy])
        posafter = np.array([-(x + vx*dt) + 2*xlignbetween23, y + vy*dt])
    elif check == 3:
        speedafter = np.array([vx, -vy])
        posafter = np.array([x + vx*dt, -(y + vy*dt) + 2*ylignbetween34])
    elif check == 4:
        speedafter = np.array([-vx, vy])
        posafter = np.array([-(x + vx*dt) + 2*xlignbetween41, y + vy*dt])
    elif check == 11:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*xlignbetween41, -(y + vy*dt) + 2*ylignbetween12])
    elif check == 22:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*xlignbetween23, -(y + vy*dt) + 2*ylignbetween12])
    elif check == 33:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*xlignbetween23, -(y + vy*dt) + 2*ylignbetween34])
    elif check == 44:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*xlignbetween41, -(y + vy*dt) + 2*ylignbetween34])
    return (posafter, speedafter)


'''script de test
theta = -np.pi/2
energy = 0.1 #energie de la frappe
dt = 0.1 #pas de temps
B = Board()
Ball = Ball(1, np.array([0.02, 0.02])) #position initial proche du coin en bas à gauche
Cue = Cue(1)
Cue.frappe(energy, theta, Ball)
print(Ball.speed)
print(Ball.position)
print(rebond(B, Ball, dt))
'''