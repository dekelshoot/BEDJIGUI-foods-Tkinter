import sqlite3  # Module pour interagir avec les bases de données SQLite


class Table:
    """
    Représente une table de commandes liée à des menus dans une base de données SQLite.
    """

    # Déclaration des attributs de classe
    id = None
    id_commande = None
    id_menu = None
    quantite = None
    prix = None
    date = None

    def __init__(self, db_name):
        """
        Initialise une connexion à la base de données SQLite et crée la table si elle n'existe pas.
        
        Args:
            db_name (str): Le nom de la base de données SQLite.
        """
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table table si elle n'existe pas déjà
    
    def create_table(self):
        """
        Crée la table 'table_list' dans la base de données si elle n'existe pas déjà.
        """
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS table_list (
            id_commande INTEGER,
            id_menu INTEGER,
            quantite INTEGER,
            prix REAL,
            date TEXT,
            PRIMARY KEY (id_commande, id_menu),
            FOREIGN KEY (id_menu) REFERENCES menu(id),
            FOREIGN KEY (id_commande) REFERENCES commande(id));
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, id_commande, id_menu, quantite, prix, date, id=None):
        """
        Ajoute les informations de la table aux attributs de l'objet.

        Args:
            id_commande (int): L'identifiant de la commande.
            id_menu (int): L'identifiant du menu.
            quantite (int): La quantité commandée.
            prix (float): Le prix de la commande.
            date (str): La date de la commande.
            id (int, optionnel): L'identifiant de la table.
        """
        self.id_commande = id_commande
        self.id_menu = id_menu
        self.quantite = quantite
        self.prix = prix
        self.date = date
        if id is not None:
            self.id = id

    def save(self):
        """
        Ajoute la table à la base de données.

        Returns:
            str: Message indiquant que la table a été ajoutée.
        """
        self.cursor.execute('INSERT INTO table_list (id_commande, id_menu, quantite, prix, date) VALUES (?, ?, ?, ?, ?)', 
                            (self.id_commande, self.id_menu, self.quantite, self.prix, self.date))
        self.conn.commit()  # Valider la transaction

        return 'La table a été ajoutée'

    def get(self):
        """
        Récupère les informations d'une table spécifique.

        Returns:
            list: Informations de la table.
        """
        query = 'SELECT * FROM table_list WHERE id_commande = ? AND id_menu = ?'
        self.cursor.execute(query, (self.id_commande, self.id_menu))
        return self.cursor.fetchall()

    def get_by_id(self, id_commande, id_menu):
        """
        Récupère une table spécifique par ID.

        Args:
            id_commande (int): L'identifiant de la commande.
            id_menu (int): L'identifiant du menu.

        Returns:
            list: Informations de la table.
        """
        query = 'SELECT * FROM table_list WHERE id_commande = ? AND id_menu = ?'
        self.cursor.execute(query, (id_commande, id_menu))
        return self.cursor.fetchall()

    def get_by_champ(self, champ, value):
        """
        Récupère les tables par un champ spécifique.

        Args:
            champ (str): Le champ à rechercher.
            value (str): La valeur du champ.

        Returns:
            list: Informations des tables correspondant au champ.
        """
        query = f'SELECT * FROM table_list WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_by_2_champ(self, champ1, champ2, value1, value2):
        """
        Récupère les tables par deux champs spécifiques.

        Args:
            champ1 (str): Le premier champ à rechercher.
            champ2 (str): Le deuxième champ à rechercher.
            value1 (str): La valeur du premier champ.
            value2 (str): La valeur du deuxième champ.

        Returns:
            list: Informations des tables correspondant aux champs.
        """
        query = f'SELECT * FROM table_list WHERE {champ1} = ? AND {champ2} = ?'
        self.cursor.execute(query, (value1, value2))
        return self.cursor.fetchall()

    def get_all(self):
        """
        Récupère toutes les tables.

        Returns:
            list: Informations de toutes les tables.
        """
        self.cursor.execute('SELECT * FROM table_list')
        return self.cursor.fetchall()

    def delete(self):
        """
        Supprime la table.
        """
        self.cursor.execute('DELETE FROM table_list WHERE id_commande = ? AND id_menu = ?', (self.id_commande, self.id_menu))
        self.conn.commit()

    def delete_with_command_id(self, command_id):
        """
        Supprime toutes les tables d'une commande.

        Args:
            command_id (int): L'identifiant de la commande.

        Returns:
            str: Message indiquant que toutes les tables ont été supprimées.
        """
        self.cursor.execute("DELETE FROM table_list WHERE id_commande = ?", (command_id,))
        self.conn.commit()
        return 'Tous les tables ont été supprimés'

    def delete_by_id(self, id_commande, id_menu):
        """
        Supprime une table spécifique par ID.

        Args:
            id_commande (int): L'identifiant de la commande.
            id_menu (int): L'identifiant du menu.

        Returns:
            str: Message indiquant que la suppression a été réussie.
        """
        self.cursor.execute('DELETE FROM table_list WHERE id_commande = ? AND id_menu = ?', (id_commande, id_menu))
        self.conn.commit()
        return 'Suppression réussie'

    def update(self):
        """
        Met à jour une table existante.

        Returns:
            str: Message indiquant que la mise à jour a été réussie ou que la table n'existe pas.
        """
        table = self.get_by_id(self.id_commande, self.id_menu)
        if len(table) > 0:
            self.cursor.execute('UPDATE table_list SET id_commande = ?, id_menu = ?, quantite = ?, prix = ?, date = ? WHERE id_commande = ? AND id_menu = ?', 
                                (self.id_commande, self.id_menu, self.quantite, self.prix, self.date, self.id_commande, self.id_menu))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "La table n'existe pas!!!"

    def update_by_id(self, id_commande, id_menu, quantite, prix, date):
        """
        Met à jour une table existante par ID.

        Args:
            id_commande (int): L'identifiant de la commande.
            id_menu (int): L'identifiant du menu.
            quantite (int): La quantité commandée.
            prix (float): Le prix de la commande.
            date (str): La date de la commande.

        Returns:
            str: Message indiquant que la mise à jour a été réussie ou que la table n'existe pas.
        """
        table = self.get_by_id(id_commande, id_menu)
        if len(table) > 0:
            self.cursor.execute('UPDATE table_list SET id_commande = ?, id_menu = ?, quantite = ?, prix = ?, date = ? WHERE id_commande = ? AND id_menu = ?', 
                                (id_commande, id_menu, quantite, prix, date, id_commande, id_menu))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "La table n'existe pas!!!"

    def __del__(self):
        """
        Ferme la connexion à la base de données lors de la suppression de l'objet.
        """
        self.conn.close()
