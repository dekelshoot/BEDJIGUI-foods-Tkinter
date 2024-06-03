import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import shelve   # Module pour la persistance des objets Python
from datetime import datetime

from classes.contact import Contact


class ContactWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        
        # Dimensions de la fenêtre
        self.win_width = 300
        self.win_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcul pour centrer la fenêtre sur l'écran
        self.center_x = int(screen_width / 2 - self.win_width / 2)
        self.center_y = int(screen_height / 2 - self.win_height / 2)

        # Définition de la géométrie de la fenêtre et centrage
        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)  # Empêche le redimensionnement de la fenêtre
        self.title('Nous envoyer un message')  # Définition du titre de la fenêtre

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
        self.contact_conf_lb = ttk.LabelFrame(self.up_frame, text="Nous envoyer un message")
        self.contact_conf_lb.grid(column=0, row=0, pady=5, rowspan=4, columnspan=4, sticky=tk.EW)

        # Labels
        self.contact_sujet_lb = ttk.Label(self.contact_conf_lb, text="Objet:")
        self.contact_sujet_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.contact_message_lb = ttk.Label(self.contact_conf_lb, text="message")
        self.contact_message_lb.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        # Champs de saisie (Entrées)
        self.contact_sujet_ent = ttk.Entry(self.contact_conf_lb)
        self.contact_sujet_ent.grid(column=1, row=1, sticky=tk.E, padx=15)
        
        # Champ de saisie pour le message
        self.contact_message_ent = tk.Text(self.contact_conf_lb,height=5, width=20)
        self.contact_message_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

 
        # Bouton pour la ajouter le contact
        self.send_btn = ttk.Button(self.contact_conf_lb, text="Envoyer", command=self.send_message)
        self.send_btn.grid(column=1, row=4, pady=5, padx=10)


    def send_message(self):
        sujet = self.contact_sujet_ent.get()
        message = self.contact_message_ent.get("1.0", tk.END).strip()

        id_utilisateur = None

        try:
            with shelve.open('utilisateur') as user:
                id_utilisateur = user['id']
        except:
            usr_resp=messagebox.showerror("Utilisateur non disponible", "Utilisateur non disponible veuillez vous connecter!!!")
            self.destroy()

        if not sujet or not message :
            messagebox.showwarning("Champs manquants", "Tous les champs doivent être remplis.")
        else:
            contact = Contact('restaurant.db')
            contact.add(id_utilisateur,sujet,message,datetime.today())
            message = contact.save()
            if message == 'Le contact a été ajouté':
                self.destroy()
                messagebox.showinfo("Succès", f"Message envoyé:\nsujet: {sujet}\nmessage: {message}\n")
                

    def destroy(self):
        # Fermer la fenêtre de manière propre
        super().destroy()