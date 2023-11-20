import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 2--------------------------------------
# --------------------------------------------------------------------------------------------

def trace(billard, dynamic_func):
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
    # Affichage de la frame
    frame_template = "frame = %i"
    frame_text = ax.text(0.01, 1.01, "", transform=ax.transAxes)

    # Création d'un dictionnaire des boules et ajout sur le graphique
    circles = {key: plt.Circle(tuple(ball.position), ball.radius, color="red") for key, ball in balls.items()}

    def init():
        """Fonction initialisant l'affichage"""
        ax.add_patch(
            plt.Rectangle((0, 0), board.corners[2][0], board.corners[2][1], edgecolor="black", facecolor="#32a852",
                          fill=True))
        for circle in circles.values():
            ax.add_patch(circle)
        return ax, circles

    def update(frame):
        """Fonction mettant à jour la position des boules"""
        # Il faut encore appeler la fonction de mise à jour de position, qui n'est pas encore créée.
        dynamic_func()
        for key in balls:
            circles[key].set_center(tuple(balls[key].position))
        frame_text.set_text(frame_template % frame)
        return circles, frame_text

    ani = FuncAnimation(fig, update, init_func=init, interval=1000 / 60, cache_frame_data=False)
    return fig, ani


"""from objet import *
animation = trace(Pool(4), lambda: None)
plt.show()"""
