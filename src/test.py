import tkinter as tk
from tkinter import ttk

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant App")
        self.root.attributes('-fullscreen', True)  # Pour afficher en plein écran

        # Couleurs
        background_color = "#FFD700"  # Or
        button_color = "#006400"  # Vert foncé
        text_color = "#FFFFFF"  # Blanc

        # Création du cadre principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.configure(bg=background_color)  # Définition de la couleur de fond

        # Titre
        title_label = ttk.Label(self.main_frame, text="Bienvenue au Restaurant XYZ", font=("Helvetica", 40), foreground=text_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=50)
        title_label.configure(background=background_color)  # Définition de la couleur de fond

        # Description
        description_label = ttk.Label(self.main_frame, text="Nous sommes ravis de vous accueillir dans notre restaurant. Découvrez notre délicieux menu et passez une commande dès maintenant !", font=("Helvetica", 20), wraplength=1000, foreground=text_color)
        description_label.grid(row=1, column=0, columnspan=2, pady=20)
        description_label.configure(background=background_color)  # Définition de la couleur de fond

        # Bouton de commande pour voir le menu
        menu_button = ttk.Button(self.main_frame, text="Voir le Menu", command=self.show_menu, style="Custom.TButton")
        menu_button.grid(row=2, column=0, padx=50, pady=30)

        # Bouton de commande pour passer une commande
        order_button = ttk.Button(self.main_frame, text="Passer une Commande", command=self.place_order, style="Custom.TButton")
        order_button.grid(row=2, column=1, padx=50, pady=30)

        # Style pour les boutons
        style = ttk.Style()
        style.configure("Custom.TButton", foreground=text_color, background=button_color, font=("Helvetica", 18))

    def show_menu(self):
        # Fonction pour afficher le menu
        pass

    def place_order(self):
        # Fonction pour passer une commande
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
