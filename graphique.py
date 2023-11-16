import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 2--------------------------------------
# --------------------------------------------------------------------------------------------

def trace(Pool):
    """Fonction générant le billard animé"""
    # Pour fermer des plots potentiellement existants
    plt.close()
    # Initialisation de la figure contenant l'animation
    fig = plt.figure("Billard Interactif Techniquement Exploitable")
    # Valeurs récupérées 
    
    def init():
        """Fonction initialisant l'affichage"""

    def update(frame):
        """Fonction générant une image de l'animation"""
    
    ani = FuncAnimation(fig, update, init_func=init, interval=1000/60, blit=True, repeat=False)
    plt.show()




