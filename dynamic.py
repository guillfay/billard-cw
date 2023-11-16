import objet as o 
import numpy as np

def update_pool(pool,deltaT):
    #version initiale sans rebond et sans interactions entre les boules et sans frottements
    balls = pool.balls
    for ball in balls.values():
        ball.update_position(ball.position + deltaT*ball.speed)

billard = o.Pool(1)
update_pool(billard,10)
print(billard)

queue = o.Cue(1)
queue.frappe(1,0,billard.balls["0"])
update_pool(billard,52)
print(billard)