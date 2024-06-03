import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.utilisateur import Utilisateur
from composants.auth.register_window import RegisterWindow

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Dimensions de la fenêtre
        self.win_width = 360
        self.win_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcul pour centrer la fenêtre sur l'écran
        self.center_x = int(screen_width / 2 - self.win_width / 2)
        self.center_y = int(screen_height / 2 - self.win_height / 2)

        # Définition de la géométrie de la fenêtre et centrage
        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)  # Empêche le redimensionnement de la fenêtre
        self.title('Connexion')  # Définition du titre de la fenêtre

        # Cadre principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Cadre supérieur
        self.up_frame = ttk.Frame(self.main_frame)
        self.up_frame.grid(column=0, row=0, sticky=tk.NSEW)

        # Cadre inférieur
        self.down_frame = ttk.Frame(self.main_frame)
        self.down_frame.grid(column=0, row=1, sticky=tk.NSEW)

        # Label Frame pour la connexion
        self.login_conf_lb = ttk.LabelFrame(self.up_frame, text="connexion au compte")
        self.login_conf_lb.grid(column=0, row=0, pady=5, rowspan=4, columnspan=3, sticky=tk.EW)

        # Labels
        self.login_username_lb = ttk.Label(self.login_conf_lb, text="Nom d'utilisateur:")
        self.login_username_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.login_password_lb = ttk.Label(self.login_conf_lb, text="Mot de passe:")
        self.login_password_lb.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        # Champs de saisie (Entrées)
        self.login_username_ent = ttk.Entry(self.login_conf_lb)
        self.login_username_ent.grid(column=1, row=1, sticky=tk.E, padx=15)
        
        # Champ de saisie pour le mot de passe avec masquage des caractères
        self.login_password_ent = ttk.Entry(self.login_conf_lb, show='*')
        self.login_password_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

        # Bouton pour la connexion
        self.connexion_btn = ttk.Button(self.login_conf_lb, text="se connecter", command=self.login)
        self.connexion_btn.grid(column=1, row=3, pady=5, padx=10)

        # Bouton pour créer un compte
        self.register_btn = ttk.Button(self.login_conf_lb, text="créer un compte", command=self.register)
        self.register_btn.grid(column=1, row=4, pady=5, padx=10)

    def login(self):
        # Récupération des données des champs de saisie
        login_username = self.login_username_ent.get()
        login_password = self.login_password_ent.get()

        # Création d'un objet Utilisateur pour gérer la connexion
        user = Utilisateur('restaurant.db')
        message = user.login(login_username, login_password)

        # Vérification du message de retour
        if message == 'connexion réussie':
            self.destroy()  # Fermer la fenêtre si la connexion réussit
            self.master.init_accueil()
        usr_rep = messagebox.askokcancel(message, message)  # Afficher un message
        if usr_rep:
            pass

    def register(self):
        # Ouvrir une nouvelle fenêtre d'inscription
        register_win = RegisterWindow(self.master)
        register_win.attributes('-topmost', True)
        register_win.grab_set() # Mettre la nouvelle fenêtre en avant
        register_win.focus_force()
        self.destroy()

    def destroy(self):
        # Fermer la fenêtre de manière propre
        super().destroy()