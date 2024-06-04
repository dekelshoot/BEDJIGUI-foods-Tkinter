import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from classes.reservation import Reservation
import shelve  

class ReservationWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.win_width = 460
        self.win_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.center_x = int(screen_width/2 - self.win_width/2)
        self.center_y = int(screen_height/2 - self.win_height/2)

        self.geometry(f'{self.win_width}x{self.win_height}+{self.center_x}+{self.center_y}')
        self.resizable(0, 0)
        self.title('Effectuer une réservation')

        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Up frame
        self.up_frame = ttk.Frame(self.main_frame)
        self.up_frame.grid(column=0, row=0, sticky=tk.NSEW)

        # Down frame
        self.down_frame = ttk.Frame(self.main_frame)
        self.down_frame.grid(column=0, row=1, sticky=tk.NSEW)

        # Reservation Label Frame
        self.reservation_conf_lb = ttk.LabelFrame(self.up_frame, text="Réservation")
        self.reservation_conf_lb.grid(column=0, row=0, pady=5, rowspan=4, columnspan=3, sticky=tk.EW)

        # Labels
        self.reservation_nb_people_lb = ttk.Label(self.reservation_conf_lb, text="Nombre de personne:")
        self.reservation_nb_people_lb.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)

        self.reservation_date_lb = ttk.Label(self.reservation_conf_lb, text="Date bloquée:")
        self.reservation_date_lb.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        self.reservation_hours_lb = ttk.Label(self.reservation_conf_lb, text="Heure bloquée:")
        self.reservation_hours_lb.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)

        self.reservation_comment_lb = ttk.Label(self.reservation_conf_lb, text="Message:")
        self.reservation_comment_lb.grid(column=0, row=4, sticky=tk.W, padx=10, pady=10)


        #Entries
        self.reservation_nb_people_ent = ttk.Spinbox(self.reservation_conf_lb, from_=1, to=6, wrap=True, width=5, format="%02.0f")
        self.reservation_nb_people_ent.grid(column=1, row=1, sticky=tk.E, padx=15)


        # DateEntry for selecting the date
        self.reservation_date_entry = DateEntry(self.reservation_conf_lb, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, year=2023)
        self.reservation_date_entry.grid(column=1, row=2, padx=15, pady=10)  # Using grid instead of pack

        # Spinboxes for hour and minute
        self.reservation_hour_spinbox = ttk.Spinbox(self.reservation_conf_lb, from_=0, to=23, wrap=True, width=5, format="%02.0f")
        self.reservation_hour_spinbox.grid(column=1, row=3, padx=5, pady=10, sticky=tk.W)
        self.reservation_minute_spinbox = ttk.Spinbox(self.reservation_conf_lb, from_=0, to=59, wrap=True, width=5, format="%02.0f")
        self.reservation_minute_spinbox.grid(column=2, row=3, padx=5, pady=10, sticky=tk.W)

        self.reservation_comment_ent = tk.Text(self.reservation_conf_lb,height=5, width=20)
        self.reservation_comment_ent.grid(column=1, row=4, sticky=tk.E, padx=15)

        #buttons
        self.connexion_btn = ttk.Button(self.reservation_conf_lb, text="Réserver", command=self.reservation)
        self.connexion_btn.grid(column=1, row=9, pady=5, padx=10)
  

    def reservation(self):
        id_utilisateur = None

        try:
            with shelve.open('utilisateur') as user:
                id_utilisateur = user['id']
                
        except:
            usr_resp=messagebox.showerror("Utilisateur non disponible", "Utilisateur non disponible veuillez vous connecter!!!")
            self.destroy()
            return

        reservation_nb_people = self.reservation_nb_people_ent.get()
        reservation_comment = self.reservation_comment_ent.get("1.0", tk.END).strip()
        
        try:
            float(reservation_nb_people)
            float(self.reservation_hour_spinbox.get())
            float(self.reservation_minute_spinbox.get())
        except:
            messagebox.showwarning("Erreur d'entée","minutes, heure et nombre de personnes doivent être des nombres!!!")
            return
        
        reservation_hours = f"{self.reservation_hour_spinbox.get()}:{self.reservation_minute_spinbox.get()}"
        reservation_date = self.reservation_date_entry.get()
        resevation_statut = "non confirmé"

        
        
        reservation = Reservation('restaurant.db')
        reservation.add(id_utilisateur,reservation_nb_people,reservation_hours,reservation_date,resevation_statut,reservation_comment)
        message=reservation.save()
        print(message)
        if message == 'La reservation a été éffectuée':
            self.destroy()
        usr_rep=messagebox.askokcancel(message,message)
        if usr_rep:
            self.destroy()
  

        
    def destroy(self):
        super().destroy()
