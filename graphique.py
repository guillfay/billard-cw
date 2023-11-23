import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from matplotlib.transforms import Affine2D
from matplotlib.animation import FuncAnimation
from objet_game import *
from objet_game import *


# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 2--------------------------------------
# --------------------------------------------------------------------------------------------

def trace(billard, dynamic_func, queue):
    """Fonction générant le billard animé"""
    # Pour fermer des plots potentiellement existants
    plt.close()
    # Valeurs récupérées dans un objet billard de la classe Pool
    board = billard.board
    balls = billard.balls
    # Initialisation de la figure contenant l'animation
    fig = plt.figure("Billard Interactif Techniquement Exploitable", figsize=(6,8))
    ax = fig.add_subplot()
    ax.set_aspect('equal')
    plt.axis("off")
    # Affichage du billard vide sur le graphique
    ax.set_xlim(-0.1 * board.corners[2][0], 1.1 * board.corners[2][0])
    ax.set_ylim(-0.1 * board.corners[2][0], board.corners[2][1] +0.1 * board.corners[2][0])
    ax.add_patch(plt.Rectangle((-0.1 * board.corners[2][0], -0.1 * board.corners[2][0]),
                               1.2 * board.corners[2][0], board.corners[2][1] +0.2 * board.corners[2][0],
                               edgecolor="black", facecolor="#774634", fill=True))
    ax.add_patch(plt.Rectangle((0, 0), board.corners[2][0], board.corners[2][1],
                               edgecolor="black", facecolor="#32a852", fill=True))
    # Création des trous
    if billard.type_billard != 'francais':
        for pocket in billard.board.get_pockets():
            ax.add_patch(plt.Circle(tuple(pocket), radius=balls[0].radius, color='k'))
            if billard.type_billard != 'anglais':
                pos_y=0.05
            else:
                pos_y=0.2
        ax.text(-0.08 * board.corners[2][0], board.corners[2][1] +0.15 * board.corners[2][0] -0.1, "Boules hors-jeu", va='center', fontsize=6, color='black')
    # Création d'un dictionnaire des boules et ajout sur le graphique
    if billard.type_billard != 'americain':
        circles = {key: plt.Circle(tuple(ball.position), ball.radius, color=ball.color) for key, ball in balls.items()}
        for circle in circles.values():
            ax.add_patch(circle)
    # Pour le billard américain, on ajoute des numéros
    else:
        nombre_affiche = ['','9','7','12','15','8','1','6','10','3','14','11','2','13','4','5']
        circles = {key: plt.Circle(tuple(ball.position), ball.radius, color=ball.color) for key, ball in balls.items()}
        for circle in circles.values():
            ax.add_patch(circle)
        labels={key: ax.text(ball.position[0], ball.position[1], nombre_affiche[ball.number], ha='center', va='center', fontsize=5, color='white')  for key, ball in balls.items()}
    # Affichage de la queue
    rectangle = patches.Rectangle((balls[0].position[0] - balls[0].radius / 2, balls[0].position[1]), 0.02, -1, color='brown')
    ax.add_patch(rectangle)
    # Affichage de la frame
    frame_template = "frame = %i"
    frame_text = ax.text(0.01, 1.01, "", transform=ax.transAxes)
    
    def update(frame):
        """Fonction mettant à jour la position des boules et de la queue"""
        # On appelle la fonction de mise à jour des positions des boules
        dynamic_func()
        for key in balls:
            circles[key].set_center(tuple(balls[key].position))
            if billard.type_billard == 'americain' and key!=0:
                labels[key].set_position(tuple(balls[key].position))
        frame_text.set_text(frame_template % frame)
        angle = queue.angle
        if all(elements for elements in [np.all(billard.balls[k].speed==0) for k in range(billard.number_of_balls)]):
            rectangle.set_alpha(1)
        else:
            rectangle.set_alpha(0)
        rectangle.set_xy((billard.balls[0].position[0] - billard.balls[0].radius / 2, billard.balls[0].position[1]))
        transform = Affine2D().rotate_deg_around(billard.balls[0].position[0], billard.balls[0].position[1], -angle) + ax.transData
        rectangle.set_transform(transform)

        return circles, frame_text, rectangle

    ani = FuncAnimation(fig, update, interval=1000 / 144, cache_frame_data=False)
    return fig, ani
