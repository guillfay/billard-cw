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
    print(board)
    # Initialisation de la figure contenant l'animation
    fig = plt.figure("Billard Interactif Techniquement Exploitable")
    ax = fig.add_subplot()
    ax.set_aspect('equal')
    ax.set_xlim(-0.1 * board.corners[2][0], 1.1 * board.corners[2][0])
    ax.set_ylim(-0.1 * board.corners[2][1], 1.1 * board.corners[2][1])
    frame_template = 'frame = %i'  # affichage dela frame
    frame_text = ax.text(0.01, 1.01, '', transform=ax.transAxes)

    # création d'un dictionnaire des boules et ajout sur le graphique
    circles = {key: plt.Circle(tuple(ball.position), ball.radius, color="red") for key, ball in balls.items()}
    for circle in circles.values():
        ax.add_patch(circle)

    def init():
        """Fonction initialisant l'affichage"""
        line1, = ax.plot([board.corners[0][0], board.corners[1][0]], [board.corners[0][1], board.corners[1][1]],
                         linestyle="-", color="black")
        line2, = ax.plot([board.corners[1][0], board.corners[2][0]], [board.corners[1][1], board.corners[2][1]],
                         linestyle="-", color="black")
        line3, = ax.plot([board.corners[2][0], board.corners[3][0]], [board.corners[2][1], board.corners[3][1]],
                         linestyle="-", color="black")
        line4, = ax.plot([board.corners[3][0], board.corners[0][0]], [board.corners[3][1], board.corners[0][1]],
                         linestyle="-", color="black")
        lines = [line1, line2, line3, line4]
        return lines

    def update(frame):
        """Fonction mettant à jour la position des boules"""
        # Il faut encore appeler la fonction de mise à jour de position, qui n'est pas encore créée.
        dynamic_func()
        for key in balls:
            circles[key].set_center(tuple(balls[key].position))
        frame_text.set_text(frame_template % frame)
        return circles, frame_text

    ani = FuncAnimation(fig, update, init_func=init, interval=1000 / 60, cache_frame_data=False)
    return ani

if __name__ == "main":
    from objet import *
    animation = trace(Pool(2), lambda: None)
    plt.show()
