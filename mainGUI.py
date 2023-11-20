import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphFrame(ttk.Frame):
    def __init__(self, master, pendulum):
        super().__init__(master)
        self.widget = None
        self.master = master
        self.draw_canvas(pendulum)
