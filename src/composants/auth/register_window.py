import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.utilisateur import Utilisateur

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.win_width = 420
        self.win_height = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)
        self.title('Créer un compte ')

        #main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        #up frame
        self.up_frame = ttk.Frame(self.main_frame)
        self.up_frame.grid(column=0, row=0, sticky=tk.NSEW)

        #down frame
        self.down_frame = ttk.Frame(self.main_frame)
        self.down_frame.grid(column=0, row=1, sticky=tk.NSEW)

        #register Label Frame
        self.register_conf_lb= ttk.LabelFrame(self.up_frame, text="connexion au compte")
        self.register_conf_lb.grid(column=0, row=0, pady=5, rowspan=4, columnspan=3, sticky=tk.EW)

        #Labels
        self.register_name_lb = ttk.Label(self.register_conf_lb, text="Nom:")
        self.register_name_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.register_prenom_lb = ttk.Label(self.register_conf_lb, text="Prenom:")
        self.register_prenom_lb.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        self.register_username_lb = ttk.Label(self.register_conf_lb, text="Nom d'utilisateur:")
        self.register_username_lb.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        self.register_password_lb = ttk.Label(self.register_conf_lb, text="Mot de passe:")
        self.register_password_lb.grid(column=0, row=4, sticky=tk.W, padx=10, pady=10)

        self.register_confirm_password_lb = ttk.Label(self.register_conf_lb, text="Confirmez le Mot de passe:")
        self.register_confirm_password_lb.grid(column=0, row=5, sticky=tk.W, padx=10, pady=10)

        self.register_email_lb = ttk.Label(self.register_conf_lb, text="Email:")
        self.register_email_lb.grid(column=0, row=6, sticky=tk.W, padx=10, pady=10)

        self.register_telephone_lb = ttk.Label(self.register_conf_lb, text="Téléphone:")
        self.register_telephone_lb.grid(column=0, row=7, sticky=tk.W, padx=10, pady=10)

        self.register_adresse_lb = ttk.Label(self.register_conf_lb, text="Adresse:")
        self.register_adresse_lb.grid(column=0, row=8, sticky=tk.W, padx=10, pady=10)

        #Entries
        self.register_name_ent = ttk.Entry(self.register_conf_lb)
        self.register_name_ent.grid(column=1, row=1, sticky=tk.E, padx=15)

        self.register_prenom_ent = ttk.Entry(self.register_conf_lb)
        self.register_prenom_ent.grid(column=1, row=2, sticky=tk.E, padx=15)

        self.register_username_ent = ttk.Entry(self.register_conf_lb)
        self.register_username_ent.grid(column=1, row=3, sticky=tk.E, padx=15)

        self.register_password_ent = ttk.Entry(self.register_conf_lb)
        self.register_password_ent.grid(column=1, row=4, sticky=tk.E, padx=15)

        self.register_confirm_password_ent = ttk.Entry(self.register_conf_lb)
        self.register_confirm_password_ent.grid(column=1, row=5, sticky=tk.E, padx=15)

        self.register_email_ent = ttk.Entry(self.register_conf_lb)
        self.register_email_ent.grid(column=1, row=6, sticky=tk.E, padx=15)

        self.register_telephone_ent = ttk.Entry(self.register_conf_lb)
        self.register_telephone_ent.grid(column=1, row=7, sticky=tk.E, padx=15)

        self.register_adresse_ent = ttk.Entry(self.register_conf_lb)
        self.register_adresse_ent.grid(column=1, row=8, sticky=tk.E, padx=15)

        #buttons
        self.connexion_btn = ttk.Button(self.register_conf_lb, text="se connecter", command=self.register)
        self.connexion_btn.grid(column=1, row=9, pady=5, padx=10)
  

    def register(self):
        register_name = self.register_name_ent.get()
        register_prenom = self.register_prenom_ent.get()
        register_username = self.register_username_ent.get()
        register_password = self.register_password_ent.get()
        register_confirm_password = self.register_confirm_password_ent.get()
        register_email = self.register_email_ent.get()
        register_telephone = self.register_telephone_ent.get()
        register_adresse = self.register_adresse_ent.get()

        if register_password == register_confirm_password :
            user = Utilisateur('restaurant.db')
            user.add(register_name, register_prenom, register_username, register_password,register_email, register_telephone, register_adresse)
            message=user.register()
            if message == 'Le compte a été créé':
                self.destroy()
            usr_rep=messagebox.askokcancel(message,message)
            if usr_rep:
                pass      
        else:
            usr_rep=messagebox.askokcancel("le mot de passe ne correspond pas","le mot de passe ne correspond pas")
          
        
    def destroy(self):
        super().destroy()
