import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
    # Affichage du billard vide sur le graphique
    ax.set_xlim(-0.1 * board.corners[2][0], 1.1 * board.corners[2][0])
    ax.set_ylim(-0.1 * board.corners[2][1], 1.1 * board.corners[2][1])
    ax.add_patch(plt.Rectangle((0, 0), board.corners[2][0], board.corners[2][1],
                               edgecolor="black", facecolor="#32a852", fill=True))
    # Création des trous
    if billard.type_billard != 'francais':
        for pocket in billard.board.get_pockets():
            ax.add_patch(plt.Circle(tuple(pocket), radius=balls[0].radius, color='k'))
    # Création d'un dictionnaire des boules et ajout sur le graphique
    circles = {key: plt.Circle(tuple(ball.position), ball.radius, color=ball.color) for key, ball in balls.items()}
    for circle in circles.values():
        ax.add_patch(circle)
    # Affichage de la frame
    frame_template = "frame = %i"
    frame_text = ax.text(0.01, 1.01, "", transform=ax.transAxes)

    queue = patches.Rectangle((billard.balls[0].position[0] - 0.02 / 2, billard.balls[0].position[1]), 0.02, -10)
    ax.add_patch(queue)

    def update(frame):
        """Fonction mettant à jour la position des boules"""
        # On appelle la fonction de mise à jour des positions des boules
        dynamic_func()
        for key in balls:
            circles[key].set_center(tuple(balls[key].position))
        frame_text.set_text(frame_template % frame)
        return circles, frame_text

    ani = FuncAnimation(fig, update, interval=1000 / 60, cache_frame_data=False)
    return fig, ani
