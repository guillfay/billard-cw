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
    board = billard.board
    balls = billard.balls
    # Initialisation de la figure contenant l'animation
    fig = plt.figure("Billard Interactif Techniquement Exploitable")
    ax = fig.add_subplot()
    ax.set_aspect('equal')
    ax.set_xlim(-0.1 * board.corners[2][0], 1.1 * board.corners[2][0])
    ax.set_ylim(-0.1 * board.corners[2][1], 1.1 * board.corners[2][1])
    frame_template = 'frame = %i'  # affichage dela frame
    frame_text = ax.text(0.01, 1.01, '', transform=ax.transAxes)


    def init():
        """Fonction initialisant l'affichage"""
        line1, = ax.plot([board.corners[0][0], board.corners[1][0]], [board.corners[0][1], board.corners[1][1]], linestyle="-", color="black")
        line2, = ax.plot([board.corners[1][0], board.corners[2][0]], [board.corners[1][1], board.corners[2][1]], linestyle="-", color="black")
        line3, = ax.plot([board.corners[2][0], board.corners[3][0]], [board.corners[2][1], board.corners[3][1]], linestyle="-", color="black")
        line4, = ax.plot([board.corners[3][0], board.corners[0][0]], [board.corners[3][1], board.corners[0][1]], linestyle="-", color="black")
        lines = [line1, line2, line3, line4]
        return lines

    def update(frame):
        """Fonction mettant à jour la position des boules"""
        # Il faut encore appeler la fonction de mise à jour de position, qui n'est pas encore créée.
        for ball in balls.values():
            position = ball.position
            radius = ball.radius
            circle = plt.Circle(position, radius, color="red")
            ax.add_patch(circle)
        frame_text.set_text(frame_template % frame)
        return ax, frame_text

    ani = FuncAnimation(fig, update, init_func=init, interval=1000 / 60, cache_frame_data=False)
    return ani


animation = trace(Pool(1))
plt.show()
