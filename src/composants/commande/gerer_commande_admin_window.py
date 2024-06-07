import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from classes.menu import Menu
from classes.table import Table
from classes.utilisateur import Utilisateur
from classes.commande import Commande
from composants.database import Database



class GererCommandAdminWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)



        self.win_width = 1080
        self.win_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.i = 5

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Gérer les commandes')
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
        self.command_conf_lf = ttk.LabelFrame(self.down_frame, text="Commandes")
        # self.command_conf_lf.config(width=450)
        self.command_conf_lf.grid(column=0, row=0)
        
        #TreeView 

        self.tr_v_vscr = ttk.Scrollbar(self.command_conf_lf, orient="vertical")


        self.tr_view_columns = ('id', 'menu','total','date','commentaire', 'statut')
        self.tr_view = ttk.Treeview(self.command_conf_lf, columns=self.tr_view_columns, show='headings', height=8, selectmode='browse', yscrollcommand=self.tr_v_vscr.set)
        self.tr_view.column('id', width=50, anchor=tk.CENTER)
        self.tr_view.column('menu', width=200, anchor=tk.CENTER)
        self.tr_view.column('total', width=200, anchor=tk.CENTER)
        self.tr_view.column('date', width=200, anchor=tk.CENTER)
        self.tr_view.column('commentaire', width=200, anchor=tk.CENTER)
        self.tr_view.column('statut', width=200, anchor=tk.CENTER)

        self.tr_view.heading('id', text="ID")
        self.tr_view.heading('menu', text="Menu")
        self.tr_view.heading('total', text="Total(€)")
        self.tr_view.heading('date', text="Date")  
        self.tr_view.heading('commentaire', text="Commntaire")  
        self.tr_view.heading('statut', text="Statut")    

        self.tr_view.grid(column=0,row=0, rowspan=6, columnspan=3, pady=10)

        self.tr_v_vscr.config(command=self.tr_view.yview)
        self.tr_v_vscr.grid(column=3, row=0, rowspan=6,  sticky=tk.NS)
        
        self.tr_view.bind('<ButtonRelease-1>', self.menu_selected)
        self.tr_view.bind('<Delete>', self.remove_selected)

        # add product labelframe

        self.remove_menu_lbf = ttk.LabelFrame(self.command_conf_lf, text="Actions")
        self.remove_menu_lbf.grid(column=0, row=8, pady=10, padx=5,  columnspan=3, sticky=tk.EW)


        self.menu_id_lbl = ttk.Label(self.remove_menu_lbf, text="commande sélectionnée:")
        self.menu_id_lbl.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        
        self.sel_menu_id_lbl = ttk.Label(self.remove_menu_lbf, text="-")
        self.sel_menu_id_lbl.grid(column=1, row=0, sticky=tk.W, padx=10, pady=10)

        
        self.tr_view_complete = ttk.Button(self.remove_menu_lbf, text="Completer", command=self.complete_command, state=tk.DISABLED)
        self.tr_view_complete.grid(column=2, row=0,padx=10, sticky=tk.E)

        self.tr_view_remove = ttk.Button(self.remove_menu_lbf, text="Annuler", command=self.remove_selected, state=tk.DISABLED)
        self.tr_view_remove.grid(column=3, row=0,padx=10, sticky=tk.E)
        

        
        
        
        self.retreive_menu_items()
        
    def retreive_menu_items(self):
        database = Database('restaurant.db')

        query =  '''
            SELECT DISTINCT commande.id , menu.nom, menu.prix, commande.date , commande.commentaire, commande.statut,table_list.quantite
            FROM table_list
            JOIN commande ON table_list.id_commande = commande.id
            JOIN menu ON table_list.id_menu = menu.id
            '''
        res=database.execute_query(query)
        result = []
        total= 0
        temp=[]
        print(res)
        r = list(res[0])
        id = []
        for row in res:
            if row[0] not in id:
                id.append(row[0])
        print(id)
        for i in id:
            ro = [i,"",0,"","",""]
            for row in res:
                if row[0]==i:
                    ro[1]= ro[1]+' , '+row[1]
                    ro[2]+=row[2]*row[6]
                    ro[3]= row[3]
                    ro[4]=row[4]
                    ro[5]= row[5]
            ro[1] = ro[1][2:]
            result.append(ro)            
        
        if len(result) > 0:    
            for el in result:
                self.tr_view.insert('', tk.END, iid=f"{el[0]}", values=el)
        
                                
    def menu_selected(self, event):
        try:    
            selected_item = self.tr_view.selection()[0]
            sel_item_val = self.tr_view.item(selected_item)['values']
            self.command = sel_item_val
            
            sel_menu_txt = f"{sel_item_val[0]}) "
            self.sel_menu_id_lbl.config(text="-")
            self.sel_menu_id_lbl.config(text=sel_menu_txt)
            
            self.tr_view_remove.config(state=tk.ACTIVE)
            self.tr_view_complete.config(state=tk.ACTIVE)
        except IndexError as e:
            print(e)
        
    def remove_selected(self, event=""):
        id = self.command[0]
        
        try:
            menu = Menu('restaurant.db')
            table_list = Table('restaurant.db')
            commande = Commande('restaurant.db')
            database = Database('restaurant.db')

            table_list.delete_with_command_id(id)
            message = commande.delete_by_id(id)
            print(message)
            self.tr_view.delete(*self.tr_view.get_children())
            self.retreive_menu_items()
            self.sel_menu_id_lbl.config(text="-")
            self.tr_view_remove.config(state=tk.DISABLED)

            messagebox.showinfo("Succès",message)
            
        except ValueError:
            messagebox.showerror("Erreur ", "Une erreur s'est produite lors de l'annlation de la commande'.")
        


  
        

    def complete_command(self):
        id = self.command[0]
        
        try:

            commande = Commande('restaurant.db')
            cmd = commande.get_by_id(id)[0]
            
            commande.add(cmd[1],"Complet",cmd[3],cmd[4],cmd[0])
            message = commande.update()
            print(message)
            self.tr_view.delete(*self.tr_view.get_children())
            self.retreive_menu_items()
            self.sel_menu_id_lbl.config(text="")
            self.tr_view_remove.config(state=tk.DISABLED)
            self.tr_view_complete.config(state=tk.DISABLED)

            messagebox.showinfo("Succès","Commande completée")
            
        except ValueError:
            messagebox.showerror("Erreur ", "Une erreur s'est produite lors de la completion de la commande'.")
        


   
    
    def destroy(self):
        
        super().destroy()
    

  