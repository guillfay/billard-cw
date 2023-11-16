import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from objet import *

# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 2--------------------------------------
# --------------------------------------------------------------------------------------------

def trace(billard):
    """Fonction générant le billard animé"""
    # Pour fermer des plots potentiellement existants
    plt.close()
    # Valeurs récupérées dans un objet billard de la classe Pool
    number_of_balls = billard.number_of_balls
    board = billard.board
    length = board.length
    width = board.width
    corners = board.corners
    balls = billard.balls
    # Initialisation de la figure contenant l'animation
    fig = plt.figure("Billard Interactif Techniquement Exploitable")
    ax = fig.add_subplot()
    ax.set_aspect('equal')
    ax.set_xlim(-0.1*length,1.1*length)
    ax.set_ylim(-0.1*length,width+0.1*length)
    
    def init():
        """Fonction initialisant l'affichage"""
        line1, = ax.plot([corners[0][0], corners[1][0]], [corners[0][1], corners[1][1]], linestyle="-", color="black")
        line2, = ax.plot([corners[1][0], corners[2][0]], [corners[1][1], corners[2][1]], linestyle="-", color="black")
        line3, = ax.plot([corners[2][0], corners[3][0]], [corners[2][1], corners[3][1]], linestyle="-", color="black")
        line4, = ax.plot([corners[3][0], corners[0][0]], [corners[3][1], corners[0][1]], linestyle="-", color="black")
        lines = [line1, line2, line3, line4]
        return lines

    def update(frame):
        """Fonction générant une image de l'animation"""
        # Il faut encore appeler la fonction de mise à jour de position, qui n'est pas encore créée.
        for i in range(number_of_balls):
            position = balls[str(i)].position
            radius = balls[str(i)].radius
            circle = plt.Circle(position, radius, color="red")
            ax.add_patch(circle)
        return ax

    ani = FuncAnimation(fig, update, init_func=init, interval=1000/60)
    return ani

ani = trace(Pool(5))
plt.show()


