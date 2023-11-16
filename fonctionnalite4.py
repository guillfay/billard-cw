import numpy as np

def frappe(board, puissance, angle, ball): #puissance en J, angle en rad par rapport à l'axe x
        mcue = board.mass
        vcue = np.sqrt(2*puissance/mcue)
        mball = ball.mass
        vball = mcue/mball * vcue
        ball.update_speed([np.cos(angle)*vball, np.sin(angle)*vball])

def detect(board, ball, dt):
    x = ball.position[0]
    y = ball.position[1]
    vx = ball.speed[0]
    vy = ball.speed[1]
    xp = x + vx*dt
    yp = y + vy*dt
    if yp < board.corner[0][1] and board.corner[0][0] < xp < board.corner[1][0]:
        return 1
    elif xp > board.corner[1][0] and board.corner[1][1] < yp < board.corner[2][1]:
        return 2
    elif yp > board.corner[2][1] and board.corner[0][0] < xp < board.corner[1][0]:
        return 3
    elif xp < board.corner[3][0] and board.corner[1][1] < yp < board.corner[2][1]:
        return 4
    elif board.corner[0][0] < xp < board.corner[1][0] and board.corner[1][1] < yp < board.corner[2][1]:
        return 0
    else: #ici c'est pour gagner du temps de calcul je me dis que c'est assez rare quand meme d'avoir 2 rebonds
        if yp < board.corner[0][1] and xp < board.corner[0][0]:
            return 11
        elif yp < board.corner[0][1] and xp > board.corner[1][0]:
            return 22
        if yp > board.corner[2][1] and xp > board.corner[1][0]:
            return 33
        elif yp > board.corner[2][1] and xp < board.corner[0][0]:
            return 44
        

def rebond(board, ball, dt):
    x = ball.position[0]
    y = ball.position[1]
    vx = ball.speed[0]
    vy = ball.speed[1]
    speedbefore = ball.speed
    check = detect(board, ball, dt)
    if check == 1:
        speedafter = np.array([vx, -vy])
        posafter = np.array([x + vx*dt, -(y + vy*dt) + 2*board.corner[0][1]])
    elif check == 2:
        speedafter = np.array([-vx, vy])
        posafter = np.array([-(x + vx*dt) + 2*board.corner[1][0], y + vy*dt])
    elif check == 3:
        speedafter = np.array([vx, -vy])
        posafter = np.array([x + vx*dt, -(y + vy*dt) + 2*board.corner[2][1]])
    elif check == 4:
        speedafter = np.array([-vx, vy])
        posafter = np.array([-(x + vx*dt) + 2*board.corner[3][0], y + vy*dt])
    elif check == 11:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*board.corner[0][0], -(y + vy*dt) + 2*board.corner[0][1]])
    elif check == 22:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*board.corner[1][0], -(y + vy*dt) + 2*board.corner[1][1]])
    elif check == 33:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*board.corner[2][0], -(y + vy*dt) + 2*board.corner[2][1]])
    elif check == 44:
        speedafter = np.array([-vx, -vy])
        posafter = np.array([-(x + vx*dt) + 2*board.corner[3][0], -(y + vy*dt) + 2*board.corner[3][1]])
        
#attention au double rebond
