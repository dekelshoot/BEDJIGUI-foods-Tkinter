import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from classes.menu import Menu



class GererMenuWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)



        self.win_width = 685
        self.win_height = 830
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.i = 5

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Gérer les menus')
        self.resizable(False, False)
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


        #Menu Label Frame
        self.menu_conf_lf = ttk.LabelFrame(self.down_frame, text="Menus")
        # self.menu_conf_lf.config(width=450)
        self.menu_conf_lf.grid(column=0, row=0)
        
        #TreeView 

        self.tr_v_vscr = ttk.Scrollbar(self.menu_conf_lf, orient="vertical")


        self.tr_view_columns = ('id', 'nom','description','price')
        self.tr_view = ttk.Treeview(self.menu_conf_lf, columns=self.tr_view_columns, show='headings', height=8, selectmode='browse', yscrollcommand=self.tr_v_vscr.set)
        self.tr_view.column('id', width=50, anchor=tk.CENTER)
        self.tr_view.column('nom', width=200, anchor=tk.CENTER)
        self.tr_view.column('description', width=200, anchor=tk.CENTER)
        self.tr_view.column('price', width=200, anchor=tk.CENTER)

        self.tr_view.heading('id', text="ID")
        self.tr_view.heading('nom', text="Nom")
        self.tr_view.heading('description', text="Description")
        self.tr_view.heading('price', text="Prix(€)")   

        self.tr_view.grid(column=0,row=0, rowspan=6, columnspan=3, pady=10)

        self.tr_v_vscr.config(command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)
        
        self.tr_view.bind('<ButtonRelease-1>', self.menu_selected)
        self.tr_view.bind('<Delete>', self.remove_selected)

        # add product labelframe
        self.add_menu_lbf = ttk.LabelFrame(self.menu_conf_lf, text="Mise à jour du menu")
        self.add_menu_lbf.grid(column=0, row=7, pady=10, padx=5,  columnspan=3, sticky=tk.EW)

        self.remove_menu_lbf = ttk.LabelFrame(self.menu_conf_lf, text="Supprimer le menu")
        self.remove_menu_lbf.grid(column=0, row=8, pady=10, padx=5,  columnspan=3, sticky=tk.EW)

        # Label and entrys

        self.menu_name_lbl = ttk.Label(self.add_menu_lbf, text="Nom du menu:")
        self.menu_name_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.menu_description_lbl = ttk.Label(self.add_menu_lbf, text="Description du menu:")
        self.menu_description_lbl.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.menu_price_lbl = ttk.Label(self.add_menu_lbf, text="Prix du menu:")
        self.menu_price_lbl.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        self.menu_name_entry = ttk.Entry(self.add_menu_lbf)
        self.menu_name_entry.grid(column=1, row=0, pady=10, padx=10)

        self.menu_description_entry = tk.Text(self.add_menu_lbf,height=5, width=20)
        self.menu_description_entry.grid(column=1, row=1, pady=10, padx=10)

        self.menu_price_entry = ttk.Entry(self.add_menu_lbf)
        self.menu_price_entry.grid(column=1, row=2, pady=10, padx=10)


        self.menu_id_lbl = ttk.Label(self.remove_menu_lbf, text="Menu sélecionné:")
        self.menu_id_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.sel_menu_id_lbl = ttk.Label(self.remove_menu_lbf, text="")
        self.sel_menu_id_lbl.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        #btn tr
        self.tr_view_add = ttk.Button(self.add_menu_lbf, text="Mettre à jour", command=self.update_menu, state=tk.DISABLED)
        self.tr_view_add.grid(column=2, row=0, rowspan=2, padx=10)
        
        self.tr_view_add.bind('<Return>', self.update_menu)

        self.tr_view_remove = ttk.Button(self.remove_menu_lbf, text="Supprimer", command=self.remove_selected, state=tk.DISABLED)
        self.tr_view_remove.grid(column=2, row=0,padx=10, sticky=tk.E)
        

        # Label Frame pour la connexion
        self.menu_conf_lb = ttk.LabelFrame(self.up_frame, text="Ajouter un menu")
        self.menu_conf_lb.grid(column=0, row=7, pady=10, padx=5,  columnspan=3, sticky=tk.EW)

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
        
        
        self.retreive_menu_items()
        
    def retreive_menu_items(self):
        menu = Menu('restaurant.db')
        result = menu.get_all()
        if len(result) > 0:    
            for el in result:
                self.tr_view.insert('', tk.END, iid=f"{el[0]}", values=el)
        
                                
    def menu_selected(self, event):
        try:    
            selected_item = self.tr_view.selection()[0]
            
            sel_item_val = self.tr_view.item(selected_item)['values']
            self.menu = sel_item_val
            
            sel_menu_txt = f"{sel_item_val[0]}) {sel_item_val[1]} "
            self.sel_menu_id_lbl.config(text="")
            self.sel_menu_id_lbl.config(text=sel_menu_txt)
            
            self.menu_name_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
            self.menu_name_entry.insert(0, sel_item_val[1])  # Insère le nouveau contenu
            
            self.menu_description_entry.delete("1.0", tk.END)  # Efface le contenu actuel du widget Text
            self.menu_description_entry.insert("1.0", sel_item_val[2])  # Insère le nouveau contenu

            self.menu_price_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
            self.menu_price_entry.insert(0, sel_item_val[3])  # Insère le nouveau contenu

            self.tr_view_add.config(state=tk.ACTIVE)
            self.tr_view_remove.config(state=tk.ACTIVE)
        except IndexError as e:
            print(e)


  
    def remove_selected(self, event=""):
        id = self.menu[0]
        
        try:
            menu = Menu('restaurant.db')
            message = menu.delete_by_id(id)
            
            self.tr_view.delete(*self.tr_view.get_children())
            self.retreive_menu_items()
            self.menu_name_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
            self.menu_description_entry.delete("1.0", tk.END)  # Efface le contenu actuel du widget Text
            self.menu_price_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
            self.sel_menu_id_lbl.config(text="")
            self.tr_view_remove.config(state=tk.DISABLED)

            messagebox.showinfo("Succès",message)
            
        except ValueError:
            messagebox.showerror("Erreur ", "Une erreur s'est produite lors de la suppression.")
        

    def update_menu(self, event='<Return>'):
        id = self.menu[0]
        nom = self.menu_name_entry.get()
        description = self.menu_description_entry.get("1.0", tk.END).strip()
        prix = self.menu_price_entry.get()

        if not nom or not description or not prix:
            messagebox.showwarning("Champs manquants", "Tous les champs doivent être remplis.")
        else:
            try:
                prix = float(prix)
                menu = Menu('restaurant.db')
                menu.add(nom,description,prix,id=id)
                message = menu.update()
                if message == "le menu n'existe pas!!!" or message=='Un menu avec ce nom existe déja!!!':
                    messagebox.showinfo("Erreur", message)
                if message == 'Mise à jour réussie':
                    self.tr_view.delete(*self.tr_view.get_children())
                    self.retreive_menu_items()
                    self.menu_name_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
                    self.menu_description_entry.delete("1.0", tk.END)  # Efface le contenu actuel du widget Text
                    self.menu_price_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
                    self.sel_menu_id_lbl.config(text="")
                    self.tr_view_remove.config(state=tk.DISABLED)
                    # self.tr_view.bind('<ButtonRelease-1>', self.menu_selected)
                    messagebox.showinfo("Succès", f"Article mise à jour:\nNom: {nom}\nDescription: {description}\nPrix: {prix}")
                
            except ValueError:
                messagebox.showerror("Erreur de prix", "Le prix doit être un nombre valide.")
        
        
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
                print(message)
                if message == 'le menu existe déjà':
                    messagebox.showinfo("Erreur", message)
                if message == 'Le menu a été ajouté':
                    self.tr_view.delete(*self.tr_view.get_children())
                    self.retreive_menu_items()
                    self.menu_name_ent.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
                    self.menu_description_ent.delete("1.0", tk.END)  # Efface le contenu actuel du widget Text
                    self.menu_price_entry.delete(0, tk.END)  # Efface le contenu actuel de l'entrée
                    self.menu_price_ent.delete(0, tk.END)
                    self.tr_view_remove.config(state=tk.DISABLED)
                    messagebox.showinfo("Succès", f"Article ajouté:\nNom: {nom}\nDescription: {description}\nPrix: {prix}")
                
            except ValueError:
                messagebox.showerror("Erreur de prix", "Le prix doit être un nombre valide.")

        pass

    
    def destroy(self):
        
        super().destroy()
    

  