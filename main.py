import graphique
import collision
import objet_game as objet_game
import numpy as np
import matplotlib.pyplot as plt
from functools import partial

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


#ca marche cas simple doublr choc 

'''
billard2 = objet.Pool(2,15,15)
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
#ball2 = billard2.balls[2]
for i in range(2):
    billard2.balls[i].update_position(np.array([4*i+1,1]))
billard2.balls[0].update_speed(np.array([1,0]))
#billard2.balls[2].update_speed(np.array([-1,0]))
ani = graphique.trace(billard2,partial(collision.update_real_pool,billard2,0.1,0.01))
plt.show()


#cas pas milieu 
billard2 = objet.Pool(2,15,15)
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
#for i in range(3):

billard2.balls[0].update_speed(np.array([1,0]))
billard2.balls[0].update_position(np.array([2,2]))
billard2.balls[1].update_position(np.array([6,3.5]))
ani = graphique.trace(billard2,partial(collision.update_real_pool,billard2,0.1,0.01))
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
update_real_pool(billard2,0.99)


#cas double choc milieu 
billard2 = objet.Pool(3,15,15)
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
ball2 = billard2.balls[2]
billard2.balls[2].update_position(np.array([3,2]))
billard2.balls[1].update_position(np.array([5,2]))
billard2.balls[0].update_position(np.array([4,9]))
billard2.balls[0].update_speed(np.array([0,-1]))
ani = graphique.trace(billard2,partial(collision.update_real_pool,billard2,0.1,0.01))
plt.show()


#cas double choc milieu 
billard2 = objet.Pool(3,15,15)
ball0 = billard2.balls[0]
ball1 = billard2.balls[1]
ball2 = billard2.balls[2]
billard2.balls[2].update_position(np.array([6,2]))
billard2.balls[1].update_position(np.array([2,6]))
billard2.balls[0].update_position(np.array([2,2]))
billard2.balls[1].update_speed(np.array([0,-1]))
billard2.balls[2].update_speed(np.array([-1,0]))
ani = graphique.trace(billard2,partial(collision.update_real_pool,billard2,0.01,0.01))

plt.show()

'''
billard = objet_game.Pool('americain')
billard.balls[0].update_speed(np.array([0,2]))

ani = graphique.trace(billard,partial(collision.update_real_pool,billard,0.0025,0.01))
plt.show()