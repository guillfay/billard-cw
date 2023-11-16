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
    corners = board.corners
    balls = billard.balls
    # Initialisation de la figure contenant l'animation
    fig = plt.figure("Billard Interactif Techniquement Exploitable")
    ax = fig.add_subplot()
    ax.set_aspect('equal')
    ax.set_xlim(-0.1 * corners[2][0], 1.1 * corners[2][0])
    ax.set_ylim(-0.1 * corners[2][1], 1.1 * corners[2][1])

    def init():
        """Fonction initialisant l'affichage"""
        line1, = ax.plot([corners[0][0], corners[1][0]], [corners[0][1], corners[1][1]], linestyle="-", color="black")
        line2, = ax.plot([corners[1][0], corners[2][0]], [corners[1][1], corners[2][1]], linestyle="-", color="black")
        line3, = ax.plot([corners[2][0], corners[3][0]], [corners[2][1], corners[3][1]], linestyle="-", color="black")
        line4, = ax.plot([corners[3][0], corners[0][0]], [corners[3][1], corners[0][1]], linestyle="-", color="black")
        lines = [line1, line2, line3, line4]
        return lines

    def update(frame):
        """Fonction mettant à jour la position des boules"""
        # Il faut encore appeler la fonction de mise à jour de position, qui n'est pas encore créée.
        for i in range(number_of_balls):
            position = balls[str(i)].position
            radius = balls[str(i)].radius
            circle = plt.Circle(position, radius, color="red")
            ax.add_patch(circle)
        return ax

    ani = FuncAnimation(fig, update, init_func=init, interval=1000 / 60, cache_frame_data=False)
    return ani


animation = trace(Pool(1))
plt.show()
