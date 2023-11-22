import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from objet import *
from objet_game import *
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
        self.__create_widgets(self.valider, self.tirer, billard)

    def __create_widgets(self, valider, tirer, billard):
        # Création des Labelframe groupant les entrées
        frame1 = ttk.Labelframe(self, text="Paramètres du billard")
        frame1.grid(column=0, row=0, columnspan=2, sticky="WE")
        frame2 = ttk.Labelframe(self, text="Paramètres de frappe")
        frame2.grid(column=0, row=4, columnspan=2, sticky="WE")
        frame3 = ttk.Labelframe(self, text="Paramètres d'animation")
        frame3.grid(column=0, row=6, columnspan=2, sticky="WE")
        # Création des labels descriptifs des entrées
        ttk.Label(frame1, text="Type de billard choisi :").grid(column=0, row=0)
        ttk.Label(frame1, text="Masse des boules (en kg) :").grid(column=0, row=3)
        ttk.Label(frame2, text="Angle de frappe (en °) :").grid(column=0, row=5)
        ttk.Label(frame2, text="Force de frappe (en %) :").grid(column=0, row=6)
        ttk.Label(frame3, text="Pas de temps (en s) :").grid(column=0, row=8)

        # Création des entrées
        self.choix = tk.IntVar()
        self.choix.set(1)
        self.balls = billard.balls

        self.choix1_entry = ttk.Radiobutton(frame1, text="Français", variable=self.choix, value=1)
        self.choix1_entry.grid(column=1, row=0)
        self.choix2_entry = ttk.Radiobutton(frame1, text="Américain", variable=self.choix, value=2)
        self.choix2_entry.grid(column=1, row=1)
        self.choix3_entry = ttk.Radiobutton(frame1, text="Anglais", variable=self.choix, value=3)
        self.choix3_entry.grid(column=1, row=2)
        self.masse_entry = ttk.Entry(frame1)
        self.masse_entry.grid(column=1, row=3)
        self.masse_entry.insert(0, self.balls[0].mass)
        self.validate_button = tk.Button(frame1, text="Valider paramètres", activebackground="green", fg="green", command=valider)
        self.validate_button.grid(column=0, row=4, columnspan=2)

        self.angle_entry = tk.Scale(frame2, from_=-180, to=180, orient="horizontal", length=150, tickinterval=90, resolution=1)
        self.angle_entry.grid(column=1, row=5)
        self.force_entry = tk.Scale(frame2, from_=0, to=100, orient="horizontal", length=150, tickinterval=25, resolution=1)
        self.force_entry.grid(column=1, row=6)
        self.validate_button = tk.Button(frame2, text="Tirer", activebackground="green", fg="green", command=tirer)
        self.validate_button.grid(column=0, row=7, columnspan=2)
        
        self.deltaT_entry = ttk.Entry(frame3)
        self.deltaT_entry.grid(column=1, row=8)
        
    def valider(self):
        """Fonction affichant un nouveau billard fixe"""
        choix = float(self.choix.get())
        # Création d'un nouveau billard pour afficher la prochaine frame (avec disjonction des cas)
        if choix==1 :
            # On appelle la fonction de mise en place du billard
            billard = Pool("francais")
        elif choix==2 :
            # On appelle la fonction de mise en place du billard
            billard = Pool("americain")
        elif choix==3 :
            # On appelle la fonction de mise en place du billard
            billard = Pool("anglais")
        self.update_billard(billard)

    def tirer(self):
        """Fonction permettant d'effectuer un tir"""
        C=Cue(0.2)
        C.frappe(energie=self.force_entry.get()/100000000,angle=self.angle_entry.get(),ball=self.balls[0])


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
        self.billard = Pool("francais")
        
        self.__create_widgets()

    def __create_widgets(self):
        """Création de la partie graphe
        On commence par donner des paramètres à update_pool"""
        partial_update_pool = partial(update_pool, self.billard, 1000/60)
        self.grap_frame = GraphFrame(self, self.billard, partial_update_pool)
        self.grap_frame.grid(column=0, row=0)

        """Création de la partie configuration"""
        self.input_frame = InputFrame(self, self.billard, self.update_pool_input)
        self.input_frame.grid(column=1, row=0)

    def update_pool_input(self, billard):
        """Mise à jour de l'objet billard et recréation de l'animation"""
        partial_update_pool = partial(update_pool, billard, 1000/60)
        self.billard = update_pool(billard, 0.1)
        self.grap_frame.draw_canvas(self.billard, partial_update_pool)

    def quit_me(self):
        """Je ne sais pas pourquoi il faut rajouter ça, mais ça marche.
        Permet de correctement gérer le clic sur le bouton de fermeture de la fenêtre"""
        self.quit()
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()


