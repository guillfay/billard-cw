import objet as o 
import numpy as np

def update_pool(pool,deltaT):
    #version initiale sans rebond et sans interactions entre les boules et sans frottements
    balls = pool.balls
    number_of_balls = pool.number_of_balls
    print(balls.values())
    i=0
    for ball in balls.values():
        i+=1
        print(i)
        ball.update_position(ball.position + deltaT*ball.speed)
        print(ball.position) 
        print("yo",deltaT*ball.speed)

def on_the_board(position_vector,width,length):
    if position_vector[0] > width or position_vector[0] < 0 :
        return False
    if position_vector[1] > length or position_vector[1] < 0 :
        return False
    return True

def collided(ball1,ball2):
    distance = np.sqrt((ball1.position[0]+ball2.position[0])**2+(ball1.position[1]+ball2.position[1])**2)
    radius_distance = ball1.radius + ball2.radius
    return (distance < radius_distance)

billard = o.Pool(1)
update_pool(billard,10)
print(billard)

queue = o.Cue(1)
queue.frappe(1,0,billard.balls["0"])
update_pool(billard,52)
print(billard)