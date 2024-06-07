import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import shelve

import webbrowser
from bs4 import BeautifulSoup

from classes.menu import Menu
from classes.table import Table
from classes.utilisateur import Utilisateur
from classes.commande import Commande
from composants.database import Database



class GererCommandUserWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)



        self.win_width = 890
        self.win_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.i = 5

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.title('Gérer mes commandes')
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


        self.tr_view_columns = ('id', 'menu','total','date', 'statut')
        self.tr_view = ttk.Treeview(self.command_conf_lf, columns=self.tr_view_columns, show='headings', height=8, selectmode='browse', yscrollcommand=self.tr_v_vscr.set)
        self.tr_view.column('id', width=50, anchor=tk.CENTER)
        self.tr_view.column('menu', width=200, anchor=tk.CENTER)
        self.tr_view.column('total', width=200, anchor=tk.CENTER)
        self.tr_view.column('date', width=200, anchor=tk.CENTER)
        self.tr_view.column('statut', width=200, anchor=tk.CENTER)

        self.tr_view.heading('id', text="ID")
        self.tr_view.heading('menu', text="Menu")
        self.tr_view.heading('total', text="Total(€)")
        self.tr_view.heading('date', text="Date")  
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

        
        self.tr_view_facture = ttk.Button(self.remove_menu_lbf, text="Télécharger la facture", command=self.print_receipt, state=tk.DISABLED)
        self.tr_view_facture.grid(column=2, row=0,padx=10, sticky=tk.E)

        self.tr_view_remove = ttk.Button(self.remove_menu_lbf, text="Annuler", command=self.remove_selected, state=tk.DISABLED)
        self.tr_view_remove.grid(column=3, row=0,padx=10, sticky=tk.E)
        

        
        
        
        self.retreive_menu_items()
        
    def retreive_menu_items(self):
        database = Database('restaurant.db')

        id_utilisateur = None

        try:
            with shelve.open('utilisateur') as user:
                id_utilisateur = user['id']
        except:
            usr_resp=messagebox.showerror("Utilisateur non disponible", "Utilisateur non disponible veuillez vous connecter!!!")
            self.destroy()

        query =  f'''
            SELECT DISTINCT commande.id , menu.nom, menu.prix, commande.date , commande.statut, table_list.quantite
            FROM table_list
            JOIN utilisateur ON commande.id_utilisateur = {id_utilisateur}
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
            ro = [i,"",0,"",""]
            for row in res:
                if row[0]==i:
                    ro[1]= ro[1]+' , '+row[1]
                    ro[2]+=row[2]*row[5]
                    ro[3]= row[3]
                    ro[4]=row[4]
            ro[1] = ro[1][2:]
            result.append(ro)
            # total =row[2]
            # r= list(row)
            # r[2]*=r[5]
            # if row[0] not in temp:  
            #     temp.append(row[0])
            #     for i in range(res.index(row)+2,len(res)):
            #         if res[i][0]==row[0]:
            #             if res[i][1]!=row[1]:
            #                 r[1]=r[1]+' , '+res[i][1]
            #                 r[2] +=res[i][2]*res[i][5]
                
            #     r[1] = " , ".join(list(set(r[1].replace(" ", "").split(','))))
            #     result.append(tuple(r))              
        
        print(result)
        # for row in res:
        #     total = total+(row[0]*row[1])

        
        if len(result) > 0:    
            for el in result:
                self.tr_view.insert('', tk.END, iid=f"{el[0]}", values=el)
        
                                
    def menu_selected(self, event):
        try:    
            selected_item = self.tr_view.selection()[0]
            sel_item_val = self.tr_view.item(selected_item)['values']
            self.command = sel_item_val
            print("sel_item_val",sel_item_val)
            sel_menu_txt = f"{sel_item_val[0]})"
            self.sel_menu_id_lbl.config(text="-")
            self.sel_menu_id_lbl.config(text=sel_menu_txt)
            
            self.tr_view_remove.config(state=tk.ACTIVE)
            self.tr_view_facture.config(state=tk.ACTIVE)
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
        

    def html_order(self, top_pad,name, quantity, price):
        p_name = f"<span style='top:{150+(top_pad * 20)}pt; left:85pt; position:absolute; font-size:20pt;'>{name}</span>"
        p_quantity = f"<span style='top:{150+(top_pad * 20)}pt; left:275pt; position:absolute; font-size:20pt;'>x{quantity}</span>"
        p_price = f"<span style='top:{150+(top_pad * 20)}pt; right:85pt; position:absolute; font-size:20pt;'>{price}</span>"
        return(BeautifulSoup(p_name, "html.parser"), BeautifulSoup(p_quantity, "html.parser"), BeautifulSoup(p_price, "html.parser"))
  
    def print_receipt(self):
        id = self.command[0]
        tags = []
        ind = 1
        tot_p = 0
        tot_q = 0

        database = Database('restaurant.db')

        query =f"""
            SELECT menu.nom,table_list.quantite, menu.prix
            FROM menu
            INNER JOIN table_list ON menu.id = table_list.id_menu
            WHERE table_list.id_commande = {id}
            """
    
        res=database.execute_query(query)
        print(res)
        total=0
        for re in res:
            total+= re[2]
            val = re
            tot_p += float(val[2]*val[1])
            tot_q += int(val[1])
            tag = self.html_order(ind, val[0], val[1], val[2])
            tags.append(tag)
            ind += 1
        total_price = f"<span style='top:{170+(len(tags) * 40)}pt; left:85pt; position:absolute; font-size:20pt;'>Total à payer: {tot_p} €</span>"
        
        with open("order_template.html") as html_doc:
            doc = BeautifulSoup(html_doc, 'html.parser')
            doc.find(text="Fac_name").replace_with("BEDJIGUI foods")
            doc.find(text="t_num").replace_with("merci pour la confiance :)")
            for tag in tags:
                doc.div.append(tag[0])
                doc.div.append(tag[1])
                doc.div.append(tag[2])
            doc.div.append(BeautifulSoup(f"<hr style='top:{170+(len(tags)*30)}pt;' />", "html.parser"))
            doc.div.append(BeautifulSoup(total_price, "html.parser"))
            
            str_doc = str(doc.prettify())
        with open("order_bedjiguifoods.html", "w+", encoding='utf-8') as p_or_fl:
            p_or_fl.write(str_doc)
            
        webbrowser.open_new_tab("order_bedjiguifoods.html")
        

   
    
    def destroy(self):
        
        super().destroy()
    

  