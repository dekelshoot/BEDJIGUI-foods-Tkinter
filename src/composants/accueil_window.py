# Importation des modules nécessaires
import tkinter as tk  # Interface graphique
from tkinter import ttk  # Widgets stylisés pour tkinter
from PIL import ImageTk, Image  # Gestion des images
from sqlite3 import Error  # Gestion des erreurs SQLite
import shelve

from composants.database import Database
from composants.apropos_window import AproposWindow
from composants.auth.login_window import LoginWindow
from composants.menu.aujout_menu_window import AjoutMenuWindow
from composants.menu.gerer_menu_window import GererMenuWindow
from composants.commande.passer_commande_window import PasserCommand
from composants.commande.gerer_commande_admin_window import GererCommandAdminWindow
from composants.commande.gerer_commande_user_window import GererCommandUserWindow
from composants.reservation.effectuer_reservation_window import ReservationWindow


class AccueilWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Définition des dimensions de la fenêtre
        self.win_width = 1920
        self.win_height = 1080
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcul pour centrer la fenêtre sur l'écran
        self.center_x = int(screen_width / 2 - self.win_width / 2)
        self.center_y = int(screen_height / 2 - self.win_height / 2)

        # Configuration de la géométrie de la fenêtre
        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)  # Fenêtre non redimensionnable
        self.title('BEDJIGUI foods')  # Titre de la fenêtre

        # Création d'un cadre principal
        self.m_frame = ttk.Frame(self, width=1920, height=1080)
        self.m_frame.grid(row=0, column=0, sticky=tk.NSEW)

        # Configuration de l'icône de la fenêtre
        self.iconphoto(True, tk.PhotoImage(file='../assets/icon_m.png'))

        # Création de la barre de menu
        self.menubar = tk.Menu(self.m_frame)

        # Menu "File"
        self.filebar = tk.Menu(self.menubar, tearoff=0)

        ### Menus
        self.menumenu = tk.Menu(self.menubar, tearoff=0)
        self.menumenu.add_command(label="Ajouter un menu", command=self.ajout_menu_window)
        self.menumenu.add_command(label="Gérer les menus", command=self.gerer_menu_window)
        self.filebar.add_cascade(label="Menu", menu=self.menumenu)
        self.filebar.add_command(label="Gérer les commandes", command=self.gerer_command_admin_window)

        self.filebar.add_separator()
        self.filebar.add_command(label="login", command=self.login_window)
        self.filebar.add_command(label="logout", command=self.logout_window)
        # self.filebar.add_command(label="Print Receipts", command=self.print_win, state=tk.DISABLED)
        # self.filebar.add_command(label="Kitchen", command=self.kitchen_win, state=tk.DISABLED)
        # self.filebar.add_command(label="Create Orders", command=self.customer_win, state=tk.DISABLED)
        # self.filebar.add_command(label="Configure Facility/Menu...", command=self.config_window)
        # # self.filebar.add_cascade(label="Configure Facility/Menu", command=self.config_window)
        # self.filebar.add_separator()
        self.filebar.add_cascade(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filebar)

        # Menu Reservation
        self.reservationmenu = tk.Menu(self.menubar, tearoff=0)
        self.reservationmenu.add_command(label="Effectuer une réservattion...", command=self.reservation_window)
        self.reservationmenu.add_command(label="Mes réservations...", command=self.apropos_window)
        self.menubar.add_cascade(label="Réservations", menu=self.reservationmenu)

        # Menu "Commande"
        self.commandemenu = tk.Menu(self.menubar, tearoff=0)
        self.commandemenu.add_command(label="Passer une commande...", command=self.passer_command_window)
        self.commandemenu.add_command(label="Gérer mes commandes...", command=self.gerer_command_user_window)
        self.menubar.add_cascade(label="Commande", menu=self.commandemenu)

        # Menu "About"
        self.contactmenu = tk.Menu(self.menubar, tearoff=0)
        self.contactmenu.add_command(label="Nous contacter...", command=self.apropos_window)
        self.menubar.add_cascade(label="Contact", menu=self.contactmenu)

        # Menu "About"
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=self.apropos_window)
        self.menubar.add_cascade(label="About", menu=self.helpmenu)

        # Configuration de la barre de menu
        self.config(menu=self.menubar)

        # Chargement et redimensionnement de l'image principale
        self.img = Image.open("../assets/main_win_ph.png")
        self.img = self.img.resize((250, 250), Image.Resampling.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        
        # Ajout de l'image et du texte à un label
        self.panel = tk.Label(self.m_frame, image=self.img, text="BEDJIGUI FOODS", compound='top', font=("Helvetica Bold", 20))
        self.panel.image = self.img
        self.panel.grid(row=0, column=0, sticky=tk.NSEW, padx=800, pady=300)

        # Ajout d'une étiquette pour la version
        self.vers = tk.Label(self.m_frame, text="v0.1,", font=("Helvetica", 8))
        self.vers.grid(row=1, column=0, sticky=tk.SW, padx=10)

        #Vérification de la base de données
        self.check_databases()
        self.reservation_window()

    
    
    def check_databases(self):
        try:
            # Connexion à la base de données
            Database("restaurant.db")
        except Error as e:
            print(e)
    
    # Méthode pour ouvrir la fenêtre "About"
    def apropos_window(self):
        about_win = AproposWindow(self)
        about_win.grab_set()
    
    # Méthode pour ouvrir la fenêtre "ajouter menu"
    def ajout_menu_window(self):
        ajout_menu_win = AjoutMenuWindow(self)
        ajout_menu_win.grab_set()

    # Méthode pour ouvrir la fenêtre "gerer les menus"
    def gerer_menu_window(self):
        ajout_menu_win = GererMenuWindow(self)
        ajout_menu_win.grab_set()
    
    # Méthode pour ouvrir la fenêtre "passer les commandes"
    def passer_command_window(self):
        passer_command = PasserCommand(self)
        passer_command.grab_set()
    
    # Méthode pour ouvrir la fenêtre "gérer  les commandes (admin)"
    def gerer_command_admin_window(self):
        gerer_command_admin = GererCommandAdminWindow(self)
        gerer_command_admin.grab_set()
    
    # Méthode pour ouvrir la fenêtre "gérer  les commandes (utilisateur)"
    def gerer_command_user_window(self):
        gerer_command_user = GererCommandUserWindow(self)
        gerer_command_user.grab_set()

    # Méthode pour ouvrir la fenêtre "reservation"
    def reservation_window(self):
        reservation_win = ReservationWindow(self)
        reservation_win.grab_set()

    # Méthode pour ouvrir la fenêtre "login"
    def login_window(self):
        about_win = LoginWindow(self)
        about_win.grab_set()

    # Méthode pour ouvrir la fenêtre "login"
    def logout_window(self):
        about_win = LoginWindow(self)
        about_win.grab_set()