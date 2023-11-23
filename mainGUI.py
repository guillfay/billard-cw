import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from objet_game import *
from graphique import *
from dynamic import *



# --------------------------------------------------------------------------------------------
# --------------------------------------FONCTIONNALITE 13-------------------------------------
# --------------------------------------------------------------------------------------------

class GraphFrame(ttk.Frame):
    """Classe permettant de générer la partie graphique de la fenêtre"""

    def __init__(self, master, billard, dynamic_func, queue):
        super().__init__(master)
        self.widget = None
        self.master = master
        self.draw_canvas(billard, dynamic_func, queue)

    def draw_canvas(self, billard, dynamic_func, queue):
        """Méthode pour recréer un canvas pour l'affichage d'un billard dans une fenêtre Tkinter"""
        # On enlève les anciens widgets
        if self.widget:
            self.widget.destroy()
        # On appelle l'animation donnée par la fonction trace de graphique.py
        # Il nous faut conserver l'objet ani pour que l'animation continue de se faire.
        self.fig, self.ani = trace(billard, dynamic_func, queue)
        # On génère le canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(column=0, row=0)
        self.canvas.draw()



class InputFrame(ttk.Frame):
    """Classe permettant de générer la partie configuration de la fenêtre"""

    def __init__(self, master, billard, change_pool_func, tirer_func, angle_func):
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

        # Enregistrement des fonctions de màj
        self.change_pool_func = change_pool_func
        self.__create_widgets(self.valider, billard)
        self.app_tirer_func = tirer_func
        self.app_angle_func = angle_func

    def __create_widgets(self, valider, billard):
        # Création des Labelframe groupant les entrées
        frame1 = ttk.Labelframe(self, text="Paramètres du billard")
        frame1.grid(column=0, row=0, columnspan=2, sticky="WE")
        frame2 = ttk.Labelframe(self, text="Paramètres de frappe")
        frame2.grid(column=0, row=4, columnspan=2, sticky="WE")
        # Création des labels descriptifs des entrées
        ttk.Label(frame1, text="Type de billard choisi :").grid(column=0, row=0)
        ttk.Label(frame1, text="Masse des boules (en kg) :").grid(column=0, row=3)
        ttk.Label(frame2, text="Angle de frappe (en °) :").grid(column=0, row=5)
        ttk.Label(frame2, text="Force de frappe (en %) :").grid(column=0, row=6)

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
        self.validate_button = tk.Button(frame1, text="Valider paramètres", activebackground="green", fg="green",
                                         command=valider)
        self.validate_button.grid(column=0, row=4, columnspan=2)

        self.angle_entry = tk.Scale(frame2, from_=-180, to=180, orient="horizontal", length=180, tickinterval=90, command=self.angle_test)
        self.angle_entry.grid(column=1, row=5)
        self.force_entry = tk.Scale(frame2, from_=0, to=100, orient="horizontal", length=180, tickinterval=25,
                                    resolution=1)
        self.force_entry.grid(column=1, row=6)
        self.validate_button = tk.Button(frame2, text="Tirer", activebackground="green", fg="green", command=self.tirer)
        self.validate_button.grid(column=0, row=7, columnspan=2)
        
        self.angle = float(self.angle_entry.get())

    def valider(self):
        """Fonction affichant un nouveau billard fixe"""
        choix = float(self.choix.get())
        # Création d'un nouveau billard pour afficher la prochaine frame (avec disjonction des cas)
        match choix:
            case 1:
                new_billard = Pool("francais")
            case 2:
                new_billard = Pool("americain")
            case 3:
                new_billard = Pool("anglais")
            case _:
                raise Exception("problème avec la valeur de <choix>")
        self.change_pool_func(new_billard, Cue(0.4))

    def tirer(self):
        """ Convertion de l'energie de % en J (100%=1J ici)"""
        self.app_tirer_func(self.force_entry.get()/100)
        
    def angle_test(self, angle):
        self.app_angle_func(float(angle))



class App(tk.Tk):
    """Classe permettant de lancer l'affichage"""

    def __init__(self):
        super().__init__()
        self.title('Simulation billard')
        self.geometry('1000x820')
        self.protocol("WM_DELETE_WINDOW", self.quit_me)

        # Layout de la fenêtre
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Initialisation du billard
        self.billard = Pool("francais")
        self.queue = Cue(0.4)
        self.angle = 0
        
        self.__create_widgets()

    def __create_widgets(self):
        """Création de la partie graphe
        Pour l'affichage graphique, on crée une fonction partial qui sera appelée sans paramètre dans GraphFrame"""
        partial_update_pool = partial(update_pool, self.billard, 1 / 360)
        self.grap_frame = GraphFrame(self, self.billard, partial_update_pool, self.queue)
        self.grap_frame.grid(column=0, row=0)
        # Création de la partie configuration
        self.input_frame = InputFrame(self, self.billard, self.change_pool_on_input, self.tirer, self.new_angle)
        self.input_frame.grid(column=1, row=0)

    def change_pool_on_input(self, billard, queue):
        """Fonction pour recréer le billard lorsque l'utilisateur change le type de billard"""
        self.billard = billard
        self.queue = queue
        partial_update_pool = partial(update_pool, self.billard, 1 / 360)
        self.grap_frame.draw_canvas(self.billard, partial_update_pool, self.queue)

    def tirer(self, energie):
        """Fonction permettant d'effectuer un tir"""
        self.queue.frappe(energie=energie, ball=self.billard.balls[0])
        
    def new_angle(self, angle):
        """Fonction permettant de changer l'angle de la queue"""
        self.queue.update_angle(angle)

    def quit_me(self):
        """Je ne sais pas pourquoi il faut rajouter ça, mais ça marche.
        Permet de correctement gérer le clic sur le bouton de fermeture de la fenêtre"""
        self.quit()
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()
