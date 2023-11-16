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
    ax.set_ylim(-0.1*width,1.1*width)
    line, = ax.plot([], [], linestyle="-", color="black")
    def init():
        """Fonction initialisant l'affichage"""

    def update():
        """Fonction générant une image de l'animation"""
        for i in range(4):
            line.set_data([corners[i][0], corners[(i+1)%4][0]],[corners[i][1], corners[(i+1)%4][1]])
        return line

    ani = FuncAnimation(fig, update, init_func=init, interval=1000/60, blit=True)
    return ani

ani = trace(Pool(5))
plt.show()


