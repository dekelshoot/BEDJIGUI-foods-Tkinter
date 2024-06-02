import sqlite3  # Module pour interagir avec les bases de données SQLite


class Table:
    # Déclaration des attributs de classe
    id = None
    id_commande = None
    id_menu = None
    quantite = None
    prix = None
    date = None

    

    def __init__(self, db_name):
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table table si elle n'existe pas déjà
    
    def create_table(self):
        # Création de la table table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS table_list (
            id_commande INTEGER,
            id_menu INTEGER,
            quantite INTEGER,
            prix REAL,
            date TEXT,
            PRIMARY KEY (id_commande, id_menu),
            FOREIGN KEY (id_menu) REFERENCES menu(id)
            FOREIGN KEY (id_commande) REFERENCES commande(id));
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self,id_commande,id_menu,quantite,prix,date,id=None):
        # Ajouter les informations de la table aux attributs de l'objet
        self.id_commande = id_commande
        self.id_menu = id_menu
        self.quantite = quantite
        self.prix = prix
        self.date = date
        if id != None: self.id = id
        

    def save(self):
        # Ajouter la table à la base de données
        self.cursor.execute('INSERT INTO table_list (id_commande,id_menu,quantite,prix,date) VALUES (?, ?, ?, ?, ?)', 
                            (self.id_commande,self.id_menu,self.quantite,self.prix,self.date))
        self.conn.commit()  # Valider la transaction

        return 'La table a été ajouté'

    def get(self):
        # Récupérer les informations d'une table 
        query = 'SELECT * FROM table_list WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        # Récupérer une table spécifique par ID
        query = 'SELECT * FROM table_list WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        # Récupérer les tables par un champ spécifique (nom du table, prix, etc.)
        query = f'SELECT * FROM table_list WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()
    
    def get_by_2_champ(self, champ1,champ2, value1,value2):
        # Récupérer les tables par un champ spécifique (nom du table, prix, etc.)
        query = f'SELECT * FROM table_list WHERE {champ1} = ? AND {champ2} = ?'
        self.cursor.execute(query, (value1,value2))
        return self.cursor.fetchall()

    def get_all(self):
        # Récupérer tous les tables
        self.cursor.execute('SELECT * FROM table_list')
        return self.cursor.fetchall()

    def delete(self):
        # Supprimer le table 
        self.cursor.execute('DELETE FROM table_list WHERE id = ?', (self.id,))
        self.conn.commit()
    
    def delete_with_command_id(self,command_id):
        # Supprimer lous les tables d'une commande 
        self.cursor.execute("DELETE FROM table_list WHERE id_commande = ?", (command_id,))
        self.conn.commit()
        return 'tous les tables ont été supprimé"'

    def delete_by_id(self, id):
        # Supprimer un table spécifique par ID
        self.cursor.execute('DELETE FROM table_list WHERE id = ?', (id,))
        self.conn.commit()
        return 'suppréssion réussie '

    def update(self):
        # Vérifier si le table existe déjà
        table = self.get_by_id(self.id)
        if len(table) > 0:
            self.cursor.execute('UPDATE table_list SET  id_commande = ?, id_menu = ?, quantite = ?, prix = ?,date = ? WHERE id = ?', (self.id_commande,self.id_menu,self.quantite,self.prix,self.date, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "la table n'existe pas!!!"

            
        
    
        

    def update_by_id(self, id, id_commande, quantite, id_menu, prix,date):
        # Vérifier si le table existe déjà
        table = self.get_by_id(self.id)
        if len(table) > 0:
            self.cursor.execute('UPDATE table_list SET  id_commande = ?, id_menu = ?, quantite = ?, prix = ?,date = ? WHERE id = ?', (id_commande,id_menu,quantite,prix,date, id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "la table n'existe pas!!!"
    
    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
