import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db):
        # Connexion à la base de données SQLite et création de l'objet curseur
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        
        # Création des tables si elles n'existent pas déjà
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
                commentaire TEXT,
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
            """)

        # Valider les changements dans la base de données
        self.conn.commit()

    def create_table(self, create_table_query):
        try:
            # Exécuter une requête pour créer une table avec le script SQL donné
            cursor = self.cur
            cursor.execute(create_table_query)
            # Valider les changements dans la base de données
            self.conn.commit()
        except Error as e:
            # En cas d'erreur, afficher l'erreur
            print(e)

    def execute_query(self, query):
        # Exécuter une requête SQL donnée et retourner les résultats
        self.cur.execute(query)
        return self.cur.fetchall()

    def update(self, update_query, values):
        try:
            # Exécuter une requête de mise à jour avec les valeurs données
            con = self.cur
            con.execute(update_query, values)
            # Valider les changements dans la base de données
            self.conn.commit()
        except Error as e:
            # En cas d'erreur, afficher l'erreur
            print(e)

    def read_val(self, read_query, table_num=''):
        try:
            # Exécuter une requête de lecture avec le numéro de table optionnel
            con = self.cur
            if "WHERE" in read_query:
                con.execute(read_query, table_num)
                rows = con.fetchall()
            else:
                con.execute(read_query)
                rows = con.fetchall()
            return rows
        except Error as e:
            # En cas d'erreur, afficher l'erreur
            print(e)

    def delete_val(self, delete_query, item_id):
        try:
            # Exécuter une requête de suppression avec l'ID de l'élément à supprimer
            con = self.cur
            con.execute(delete_query, item_id)
            # Valider les changements dans la base de données
            self.conn.commit()
        except Error as e:
            # En cas d'erreur, afficher l'erreur
            print(e)

    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
