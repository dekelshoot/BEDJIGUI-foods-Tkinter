import tkinter as tk
from tkinter import ttk
# from ctypes import windll
# windll.shcore.SetProcessDpiAwareness(1)


class AproposWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.win_width = 360
        self.win_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)
        self.title('Apropos de l\'application')

        about_lbl = ttk.Label(self, wraplength=300, justify='left', padding=(5,20, 0, 0), font=("Helvetica Bold", 12),text="Cette application a été développée par BEDJIGUI foods en tant que projet final pour le cours de programmation orienté objet de l'école industrielle et commerciale de la Province de Namur, dispensé par madame Tchana Philomène. \n\nLa fonctionnalité principale de cette application consiste à gérer le système d'un restaurant, à faciliter le processus de commande entre le client et le chef de cuisine. Date de développement : Mai 2024.")
        about_lbl.pack()
