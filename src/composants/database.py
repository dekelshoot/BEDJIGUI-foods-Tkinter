
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS utilisateur (
                id INTEGER PRIMARY KEY, 
                nom TEXT, 
                prenom TEXT, 
                nom_d_utilisateur TEXT, 
                mot_de_passe TEX,
                email TEXT, 
                telephone TEXT, 
                est_admin INTEGER,
                adresse TEXT); """)
        
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY, 
                nom TEXT, 
                description TEXT, 
                prix REAL);
            """)
        
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS reservation (
                id INTEGER PRIMARY KEY, 
                id_utilisateur INTEGER,
                nombre_personne INTEGER,
                heure TEXT,
                date TEXT,
                statut TEXT, 
                commentaire TEXT, 
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
            """)
        
        
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY, 
                id_utilisateur INTEGER,
                sujet TEXT,
                message TEXT,
                date TEXT,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));

            """)
        
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS table_list (
                id_commande INTEGER,
                id_menu INTEGER,
                quantite INTEGER,
                prix REAL,
                date TEXT,
                PRIMARY KEY (id_commande, id_menu),
                FOREIGN KEY (id_menu) REFERENCES menu(id)
                FOREIGN KEY (id_commande) REFERENCES commande(id));
            """)

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS commande (
                id INTEGER PRIMARY KEY, 
                id_utilisateur INTEGER,
                statut TEXT,
                date TEXT,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
            """)

                
        self.conn.commit()

      

    def create_table(self, create_table_query):
        try:
            cursor = self.cur
            cursor.execute(create_table_query)
            self.conn.commit()
        except Error as e:
            print(e)

    def execute_query(self,query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def update(self, update_query, values):
        try:
            con = self.cur
            con.execute(update_query, values)
            self.conn.commit()
        except Error as e:
            print(e)

    def read_val(self, read_query, table_num=''):
        try:
            con = self.cur
            if "WHERE" in read_query:
                con.execute(read_query, table_num)
                rows = con.fetchall()
            else:
                con.execute(read_query)
                rows = con.fetchall()
            return rows
        except Error as e:
            print(e)
            
    def delete_val(self, delete_query, item_id):
        try:
            con = self.cur
            con.execute(delete_query, item_id)
            self.conn.commit()
        except Error as e:
            print(e)
            
    def __del__(self):
        self.conn.close()