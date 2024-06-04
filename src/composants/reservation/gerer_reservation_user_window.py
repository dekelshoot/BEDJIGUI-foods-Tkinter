import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import shelve


from classes.reservation import Reservation




class GererReservationUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)



        self.win_width = 800
        self.win_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.i = 5

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Gérer mes réservations')
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
        self.reservation_conf_lf = ttk.LabelFrame(self.down_frame, text="Mes réservations")
        # self.reservation_conf_lf.config(width=450)
        self.reservation_conf_lf.grid(column=0, row=0)
        
        #TreeView 

        self.tr_v_vscr = ttk.Scrollbar(self.reservation_conf_lf, orient="vertical")


        self.tr_view_columns = ('id', 'nombre de personne','date','heure','commentaire', 'statut')
        self.tr_view = ttk.Treeview(self.reservation_conf_lf, columns=self.tr_view_columns, show='headings', height=8, selectmode='browse', yscrollcommand=self.tr_v_vscr.set)
        self.tr_view.column('id', width=50, anchor=tk.CENTER)
        self.tr_view.column('nombre de personne', width=200, anchor=tk.CENTER)
        self.tr_view.column('date', width=100, anchor=tk.CENTER)
        self.tr_view.column('heure', width=100, anchor=tk.CENTER)
        self.tr_view.column('commentaire', width=200, anchor=tk.CENTER)
        self.tr_view.column('statut', width=100, anchor=tk.CENTER)

        self.tr_view.heading('id', text="ID")
        self.tr_view.heading('nombre de personne', text="Nombre de personne")
        self.tr_view.heading('date', text="Date")
        self.tr_view.heading('heure', text="Heure")  
        self.tr_view.heading('commentaire', text="Commentaire")  
        self.tr_view.heading('statut', text="Statut")    

        self.tr_view.grid(column=0,row=0, rowspan=6, columnspan=3, pady=10)

        self.tr_v_vscr.config(command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)
        
        self.tr_view.bind('<ButtonRelease-1>', self.menu_selected)
        self.tr_view.bind('<Delete>', self.remove_selected)

        # add product labelframe

        self.remove_menu_lbf = ttk.LabelFrame(self.reservation_conf_lf, text="Actions")
        self.remove_menu_lbf.grid(column=0, row=8, pady=10, padx=5,  columnspan=3, sticky=tk.EW)


        self.menu_id_lbl = ttk.Label(self.remove_menu_lbf, text="reservation sélectionnée:")
        self.menu_id_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.sel_menu_id_lbl = ttk.Label(self.remove_menu_lbf, text="-")
        self.sel_menu_id_lbl.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        self.tr_view_confirm = ttk.Button(self.remove_menu_lbf, text="Confirmer", command=self.confirm_reservation, state=tk.DISABLED)
        self.tr_view_confirm.grid(column=2, row=0,padx=10, sticky=tk.E)

        self.tr_view_remove = ttk.Button(self.remove_menu_lbf, text="Annuler", command=self.remove_selected, state=tk.DISABLED)
        self.tr_view_remove.grid(column=3, row=0,padx=10, sticky=tk.E)
        

        
        
        
        self.retreive_menu_items()
        
    def retreive_menu_items(self):
        id_utilisateur = None

        try:
            with shelve.open('utilisateur') as user:
                id_utilisateur = user['id']
        except:
            usr_resp=messagebox.showerror("Utilisateur non disponible", "Utilisateur non disponible veuillez vous connecter!!!")
            self.destroy()

        reservation = Reservation('restaurant.db')


        result=reservation.get_by_champ("id_utilisateur",id_utilisateur)
        
        
        
        if len(result) > 0:    
            for el in result:
                self.tr_view.insert('', tk.END, iid=f"{el[0]}", values=el)
        
                                
    def menu_selected(self, event):
        try:
            self.tr_view_remove.config(state=tk.DISABLED)
            self.tr_view_confirm.config(state=tk.DISABLED)
            selected_item = self.tr_view.selection()[0]
            sel_item_val = self.tr_view.item(selected_item)['values']
            self.command = sel_item_val
            
            sel_menu_txt = f"{sel_item_val[0]}) {sel_item_val[1]} "
            self.sel_menu_id_lbl.config(text="-")
            self.sel_menu_id_lbl.config(text=sel_menu_txt)
            
            self.tr_view_remove.config(state=tk.ACTIVE)
            if self.command[5] != "confirmé":
                self.tr_view_confirm.config(state=tk.ACTIVE)
        except IndexError as e:
            print(e)
        
    def remove_selected(self, event=""):
        id = self.command[0]
        
        try:
            reservation = Reservation('restaurant.db')

            message = reservation.delete_by_id(id)
            print(message)
            self.tr_view.delete(*self.tr_view.get_children())
            self.retreive_menu_items()
            self.sel_menu_id_lbl.config(text="-")
            self.tr_view_remove.config(state=tk.DISABLED)
            self.tr_view_confirm.config(state=tk.DISABLED)

            messagebox.showinfo("Succès",message)
            
        except ValueError:
            messagebox.showerror("Erreur ", "Une erreur s'est produite lors de l'annlation de la reservation'.")
        



    def confirm_reservation(self):
        id = self.command[0]
        
        try:

            reservation = Reservation('restaurant.db')
            res = reservation.get_by_id(id)[0]
            reservation.add(res[1],res[2],res[3],res[4],"confirmé",res[6],id=id)
            message = reservation.update()
            print(message)
            self.tr_view.delete(*self.tr_view.get_children())
            self.retreive_menu_items()
            self.sel_menu_id_lbl.config(text="")
            self.tr_view_remove.config(state=tk.DISABLED)
            self.tr_view_confirm.config(state=tk.DISABLED)

            if message == 'Mise à jour réussie':
                messagebox.showinfo("Succès","Reservation confirmée")
            else:
                messagebox.showinfo("Erreur",message)
            
        except ValueError:
            messagebox.showerror("Erreur ", "Une erreur s'est produite lors de la confirmation de la réservation'.")
        


   
    
    def destroy(self):
        
        super().destroy()
    

  