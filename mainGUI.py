import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from objet import *
from graphique import *
from dynamic import *


# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 7--------------------------------------
# --------------------------------------------------------------------------------------------

class GraphFrame(ttk.Frame):
    """Classe permettant de générer la partie graphique de la fenêtre"""
    def __init__(self, master, billard, dynamic_func):
        super().__init__(master)
        self.widget = None
        self.master = master
        self.draw_canvas(billard, dynamic_func)
        
    def draw_canvas(self, billard, dynamic_func):
        # On enlève les anciens widgets
        if self.widget:
            self.widget.destroy()
        # On appelle l'animation donnée par la fonction trace de graphique.py
        self.fig, self.ani = trace(billard, dynamic_func)
        # On génère le canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(column=0, row=0)
        self.canvas.draw()



class InputFrame(ttk.Frame):
    """Classe permettant de générer la partie configuration de la fenêtre"""
    def __init__(self, master, billard, update_billard):
        super().__init__(master)

        # Création des colonnes et lignes pour les objets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)

        # Enregistrement des fonctions de màj
        self.update_billard = update_billard
        self.__create_widgets(self.valider, billard)

    def __create_widgets(self, valider, billard):
        # Création des Labelframe groupant les entrées
        frame1 = ttk.Labelframe(self, text="Paramètres du billard")
        frame1.grid(column=0, row=0, columnspan=2, sticky="WE")
        frame2 = ttk.Labelframe(self, text="Paramètres de frappe")
        frame2.grid(column=0, row=7, columnspan=2, sticky="WE")
        frame3 = ttk.Labelframe(self, text="Paramètres d'animation")
        frame3.grid(column=0, row=9, columnspan=2, sticky="WE")
        # Création des labels descriptifs des entrées
        ttk.Label(frame1, text="Type de billard choisi :").grid(column=0, row=0)
        ttk.Label(frame1, text="Masse des boules :").grid(column=0, row=4)
        ttk.Label(frame1, text="Rayon des boules :").grid(column=0, row=5)
        ttk.Label(frame1, text="Longueur/largeur de la table :").grid(column=0, row=6)
        ttk.Label(frame2, text="Angle de frappe :").grid(column=0, row=7)
        ttk.Label(frame2, text="Force de frappe :").grid(column=0, row=8)
        ttk.Label(frame3, text="Pas de temps :").grid(column=0, row=9)

        # Création des entrées
        self.choix = tk.IntVar()
        self.choix.set(1)
        self.n_ball = tk.IntVar()
        self.n_ball.set(3)
        self.board = billard.board
        self.balls = billard.balls

        self.choix1_entry = ttk.Radiobutton(frame1, text="Français", variable=self.choix, value=1)
        self.choix1_entry.grid(column=1, row=0)
        self.choix2_entry = ttk.Radiobutton(frame1, text="Américain", variable=self.choix, value=2)
        self.choix2_entry.grid(column=1, row=1)
        self.choix3_entry = ttk.Radiobutton(frame1, text="Anglais", variable=self.choix, value=3)
        self.choix3_entry.grid(column=1, row=2)
        self.choix4_entry = ttk.Radiobutton(frame1, text="Personnalisé", variable=self.choix, value=4)
        self.choix4_entry.grid(column=1, row=3)
        self.masse_entry = ttk.Entry(frame1)
        self.masse_entry.grid(column=1, row=4)
        self.masse_entry.insert(0, self.balls[0].mass)
        self.rayon_entry = ttk.Entry(frame1)
        self.rayon_entry.grid(column=1, row=5)
        self.rayon_entry.insert(0, self.balls[0].radius)
        self.length_entry = ttk.Entry(frame1, text="Longueur :")
        self.length_entry.grid(column=1, row=6)
        self.length_entry.insert(0, self.board.length)
        self.width_entry = ttk.Entry(frame1, text="Largeur")
        self.width_entry.grid(column=2, row=6)
        self.width_entry.insert(0, self.board.width)

        self.angle_entry = tk.Scale(frame2, from_=-180, to=180, orient="horizontal", length=150, tickinterval=90, resolution=1)
        self.angle_entry.grid(column=1, row=7)
        self.force_entry = tk.Scale(frame2, from_=0, to=100, orient="horizontal", length=150, tickinterval=25, resolution=1)
        self.force_entry.grid(column=1, row=8)
        
        self.deltaT_entry = ttk.Entry(frame3)
        self.deltaT_entry.grid(column=1, row=9)
        
        self.validate_button = tk.Button(self, text="Valider", activebackground="green", fg="green", command=valider)
        self.validate_button.grid(column=1, row=10)
    
    def valider(self):
        """Fonction affichant un nouveau billard fixe"""
        # Disjonction des cas pour le choix du type de billard
        if self.choix==1 :
            self.n_ball = 3
        elif self.choix==2 :
            self.n_ball = 16
        elif self.choix==3 :
            self.n_ball = 16
        else :
            self.n_ball = 1
        # Récupération des valeurs
        masse = float(self.masse_entry.get())
        rayon = float(self.rayon_entry.get())
        length = float(self.length_entry.get())
        width = float(self.width_entry.get())
        angle = float(self.angle_entry.get())
        force = float(self.force_entry.get())
        
        billard = Pool(3)
        for i in range(self.n_ball) :
            self.balls[i].mass = masse
            self.balls[i].radius = rayon
        self.board.length = length
        self.board.width = width
        self.board.corners = self.board.get_corners()
        billard.balls = self.balls
        billard.board = self.board
        update_pool(billard, 0)



class App(tk.Tk):
    """Classe permettant de lancer l'affichage"""
    def __init__(self):
        super().__init__()
        self.title('Simulation billard')
        self.geometry('1200x675')
        self.protocol("WM_DELETE_WINDOW", self.quit_me)

        # Layout de la fenêtre
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        
        # Initialisation du billard
        self.billard = Pool(3)
        
        self.__create_widgets()
    
    def __create_widgets(self):
        """Création de la partie graphe
        On commence par donner des paramètres à update_pool"""
        partial_update_pool = partial(update_pool, self.billard, 0)
        self.grap_frame = GraphFrame(self, self.billard, partial_update_pool)
        self.grap_frame.grid(column=0, row=0)

        """Création de la partie configuration"""
        self.input_frame = InputFrame(self, self.billard, self.update_pool_input)
        self.input_frame.grid(column=1, row=0)
        
    def update_pool_input(self):
        """Mise à jour de l'objet billard et recréation de l'animation"""
        partial_update_pool = partial(update_pool, self.billard, 0)
        self.billard = update_pool(self.billard, 0.1)
        self.grap_frame.draw_canvas(self.billard, partial_update_pool)

    def quit_me(self):
        """Je ne sais pas pourquoi il faut rajouter ça, mais ça marche.
        Permet de correctement gérer le clic sur le bouton de fermeture de la fenêtre"""
        self.quit()
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
