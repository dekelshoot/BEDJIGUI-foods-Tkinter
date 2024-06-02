import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.menu import Menu


class AjoutMenuWindow(tk.Toplevel):
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
        self.title('Ajouter un menu')  # Définition du titre de la fenêtre

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
        self.menu_conf_lb = ttk.LabelFrame(self.up_frame, text="Ajouter un menu")
        self.menu_conf_lb.grid(column=0, row=0, pady=5, rowspan=4, columnspan=4, sticky=tk.EW)

        # Labels
        self.menu_name_lb = ttk.Label(self.menu_conf_lb, text="Nom:")
        self.menu_name_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.menu_description_lb = ttk.Label(self.menu_conf_lb, text="Description")
        self.menu_description_lb.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        self.menu_price_lb = ttk.Label(self.menu_conf_lb, text="Prix")
        self.menu_price_lb.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        # Champs de saisie (Entrées)
        self.menu_name_ent = ttk.Entry(self.menu_conf_lb)
        self.menu_name_ent.grid(column=1, row=1, sticky=tk.E, padx=15)
        
        # Champ de saisie pour la description
        self.menu_description_ent = tk.Text(self.menu_conf_lb,height=5, width=20)
        self.menu_description_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

        # Champ de saisie pour le prix
        self.menu_price_ent = ttk.Entry(self.menu_conf_lb)
        self.menu_price_ent.grid(column=1, row=3, sticky=tk.E, padx=15)

        # Bouton pour la ajouter le menu
        self.connexion_btn = ttk.Button(self.menu_conf_lb, text="Ajouter le menu", command=self.add_menu)
        self.connexion_btn.grid(column=1, row=4, pady=5, padx=10)


    def add_menu(self):
        nom = self.menu_name_ent.get()
        description = self.menu_description_ent.get("1.0", tk.END).strip()
        prix = self.menu_price_ent.get()

        if not nom or not description or not prix:
            messagebox.showwarning("Champs manquants", "Tous les champs doivent être remplis.")
        else:
            try:
                prix = float(prix)
                menu = Menu('restaurant.db')
                menu.add(nom,description,prix)
                message = menu.save()
                if message == 'le menu existe déjà':
                    messagebox.showinfo("Erreur", message)
                if message == 'Le menu a été ajouté':
                    self.destroy()
                    messagebox.showinfo("Succès", f"Article ajouté:\nNom: {nom}\nDescription: {description}\nPrix: {prix}")
                
            except ValueError:
                messagebox.showerror("Erreur de prix", "Le prix doit être un nombre valide.")

        pass


    def destroy(self):
        # Fermer la fenêtre de manière propre
        super().destroy()