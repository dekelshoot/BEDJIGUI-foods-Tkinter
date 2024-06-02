import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import Error
import shelve   # Module pour la persistance des objets Python
from datetime import datetime

from composants.commande.menu_selectors import MenuSelector
from classes.menu import Menu
from classes.table import Table
from classes.utilisateur import Utilisateur
from classes.commande import Commande
from composants.database import Database

class PasserCommand(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        
        self.order_ls = []
        
        self.win_width = 600
        self.win_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('BEDJIGUI foods')
        self.resizable(0, 0)

        #main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10, ipady=5, ipadx=5)

        #Labels
        self.cst_lbl  = ttk.LabelFrame(self.main_frame, text="Passer une commande")
        self.cst_lbl.grid(column=0, row=0, columnspan=4, sticky=tk.NSEW, padx=10) 

        self.pr_sel_lbl = ttk.Frame(self.cst_lbl)
        self.pr_sel_lbl.grid(column=0, row=5, columnspan=4, rowspan=10, sticky=tk.NSEW)

        self.pr_sel_canvas = tk.Canvas(self.pr_sel_lbl, borderwidth=0, width=550, height=400)
        self.pr_sel_canvas.grid(column=0, row=0, sticky=tk.NSEW)

        self.pr_sel_canvas_frm = ttk.Frame(self.pr_sel_canvas)
        self.cst_lbl_scroller = ttk.Scrollbar(self.pr_sel_lbl, command=self.pr_sel_canvas.yview) 
        self.cst_lbl_scroller2 = ttk.Scrollbar(self.pr_sel_lbl, command=self.pr_sel_canvas.xview) 
        self.cst_lbl_scroller.grid(column=4, row=0, sticky=tk.NS)
        self.cst_lbl_scroller2.grid(column=4, row=12, sticky=tk.NS)
        self.pr_sel_canvas.configure(yscrollcommand=self.cst_lbl_scroller.set,xscrollcommand=self.cst_lbl_scroller2)
        
        self.pr_sel_canvas.create_window((5, 5), anchor=tk.NW, window=self.pr_sel_canvas_frm)

        self.pr_sel_canvas_frm.bind("<Configure>", self.onFrameConfig)
        
    

        self.pr_name = ttk.Label(self.cst_lbl, text="Menu")
        self.pr_name.grid(column=0, row=3)

        self.pr_qty = ttk.Label(self.cst_lbl, text="Quantité")
        self.pr_qty.grid(column=1, row=3)

        self.pr_st = ttk.Label(self.cst_lbl, text="Statut de la commande")
        self.pr_st.grid(column=2, row=3)

        self.row_count = tk.IntVar()
        self.row_count.set(1)

        self.total_lbl = ttk.Label(self.main_frame, text="Total:")
        self.total_lbl.grid(column=0, row=3, padx=0, pady=0)
        
        self.sel_total_lbl = ttk.Label(self.main_frame, text="-")
        self.sel_total_lbl.grid(column=0, row=3, padx=(50,0), pady=10)

        self.btn_ajouter_menu = ttk.Button(self.main_frame, text="Ajouter un menu", command=self.ajouter_menu)
        self.btn_ajouter_menu.grid(column=0, row=4, padx=(50,0), pady=10)

        self.close_btn = ttk.Button(self.main_frame,text='Fermer',command=self.destroy)
        self.close_btn.grid(column=1, row=4, padx=(50,0), pady=10)

        self.send_to_ch = ttk.Button(self.main_frame,text='Passer la commande', state=tk.DISABLED, command=self.commander)
        self.send_to_ch.grid(column=2, row=4, padx=(50,0), pady=10)
        


        
    def commander(self):
        try:
            orders = []
            for order in self.order_ls:
                if order.retrieve_data()[0] == 'Sélectionner le menu':
                    messagebox.showerror("Aucun menu sélectionné", "Veuillez remplir le champ \"Sélectionner le menu\" ou supprimer cette ligne pour continuer !")
                    return False
                else:
                    orders.append((order.retrieve_data()))
            self.enregistre_commande(orders)
            
            
        except Error as e:
            print(e)
    
    def enregistre_commande(self,orders):
        print(orders)

        menu = Menu('restaurant.db')
        table_list = Table('restaurant.db')
        commande = Commande('restaurant.db')

        id_utilisateur = None

        try:
            with shelve.open('utilisateur') as user:
                id_utilisateur = user['id']
        except:
            usr_resp=messagebox.showerror("Utilisateur non disponible", "Utilisateur non disponible veuillez vous connecter!!!")
            self.destroy()
        print(id_utilisateur)
        menus_id = []
        temp = []
        for order in orders:
            if order[0] in temp:
                messagebox.showinfo("Erreur", "Veillez regrouper les menus!!!")
                return 
            temp.append(order[0])
            m = menu.get_by_champ("nom",order[0])
            menus_id.append((m[0][0],m[0][3],int(order[1])))
        del menu


        commande.add(id_utilisateur,"en cours",datetime.today())
        commande.save()
        

        for menu in menus_id:
            table_list.add(commande.id,menu[0],menu[2],menu[1],datetime.now())
            table_list.save()
        del commande
        del table_list
        
        
        

        
        usr_resp = messagebox.askyesno("Succès", "Les commandes ont été envoyées à la cuisine, vous pouvez y accéder par la fenêtre de gestion des commandes, souhaitez-vous passer d'autres commandes ?")
        if usr_resp:
            self.clear()
        else:
            self.destroy()
            
            
    def clear(self):
        for order in self.order_ls:
            order.destroy_all2()
        self.order_ls = []
        
    def ajouter_menu(self):
        self.max = self.pr_sel_canvas_frm.grid_size()
        self.row_count.set((self.row_count.get() + 1) if self.row_count.get() >= self.max[1] else self.max[1] + 1)
        self.pr_sl = MenuSelector(self, self.pr_sel_canvas_frm,self.row_count.get(), func=self.des_pr,func2=self.des_pr2)
        self.order_ls.insert(self.row_count.get() ,self.pr_sl)
        self.send_to_ch.config(state=tk.ACTIVE)


    
    def des_pr(self,ob):
        if len(self.pr_sel_canvas_frm.winfo_children()) == 0:
            self.send_to_ch.config(state=tk.DISABLED)
            self.row_count.set(1)
            self.order_ls = []
        else:
            self.order_ls.remove(ob)
        self.set_val = self.row_count.get() - 1 if self.row_count.get() > 1 else 1
        self.row_count.set(self.set_val)
    
    def des_pr2(self):
        if len(self.pr_sel_canvas_frm.winfo_children()) == 0:
            self.send_to_ch.config(state=tk.DISABLED)
            self.row_count.set(1)
            self.order_ls = []
        self.set_val = self.row_count.get() - 1 if self.row_count.get() > 1 else 1
        self.row_count.set(self.set_val)

    
    def onFrameConfig(self, event):
        self.pr_sel_canvas.configure(scrollregion=self.pr_sel_canvas.bbox("all"))
        
    def destroy(self):
        # self.func()
        super().destroy()
        
    def __def__(self):
        self.func
