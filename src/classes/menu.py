import sqlite3  # Module pour interagir avec les bases de données SQLite


class Menu:
    """
    Classe représentant un menu dans une base de données.
    """

    # Déclaration des attributs de classe
    id = None
    nom = None
    description = None
    prix = None

    def __init__(self, db_name):
        """
        Initialise une nouvelle instance de la classe Menu.

        Args:
            db_name (str): Nom de la base de données SQLite.
        """
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table menu si elle n'existe pas déjà
    
    def create_table(self):
        """
        Crée la table menu dans la base de données si elle n'existe pas déjà.
        """
        # Création de la table menu
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY, 
            nom TEXT, 
            description TEXT, 
            prix REAL);
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, nom, description, prix, id=None):
        """
        Ajoute les informations du menu aux attributs de l'objet.

        Args:
            nom (str): Nom du menu.
            description (str): Description du menu.
            prix (float): Prix du menu.
            id (int, optional): Identifiant du menu. Défaut à None.
        """
        # Ajouter les informations du menu aux attributs de l'objet
        self.nom = nom
        self.description = description
        self.prix = prix
        if id is not None:
            self.id = id

    def save(self):
        """
        Enregistre le menu dans la base de données.

        Returns:
            str: Message indiquant que le menu a été ajouté ou existe déjà.
        """
        # Vérifier si le menu existe déjà
        menu = self.get_by_champ("nom", self.nom)
        if len(menu) > 0:
            return 'Le menu existe déjà'
        # Ajouter le menu à la base de données
        self.cursor.execute('INSERT INTO menu (nom, description, prix) VALUES (?, ?, ?)', 
                            (self.nom, self.description, self.prix))
        self.conn.commit()  # Valider la transaction

        # Récupérer le menu pour obtenir son ID
        menu = self.get_by_champ("nom", self.nom)
        self.id = menu[0][0]

        return 'Le menu a été ajouté'

    def get(self):
        """
        Récupère les informations du menu actuel depuis la base de données.

        Returns:
            list: Informations du menu.
        """
        # Récupérer les informations du menu
        query = 'SELECT * FROM menu WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        """
        Récupère un menu spécifique par son ID.

        Args:
            id (int): Identifiant du menu.

        Returns:
            list: Informations du menu.
        """
        # Récupérer un menu spécifique par ID
        query = 'SELECT * FROM menu WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        """
        Récupère les menus par un champ spécifique.

        Args:
            champ (str): Nom du champ.
            value (any): Valeur du champ.

        Returns:
            list: Liste des menus correspondant au champ et à la valeur spécifiés.
        """
        # Récupérer les menus par un champ spécifique
        query = f'SELECT * FROM menu WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        """
        Récupère tous les menus de la base de données.

        Returns:
            list: Liste de tous les menus.
        """
        # Récupérer tous les menus
        self.cursor.execute('SELECT * FROM menu')
        return self.cursor.fetchall()

    def delete(self):
        """
        Supprime le menu actuel de la base de données.
        """
        # Supprimer le menu
        self.cursor.execute('DELETE FROM menu WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        """
        Supprime un menu spécifique par son ID.

        Args:
            id (int): Identifiant du menu à supprimer.

        Returns:
            str: Message indiquant que la suppression a été réussie.
        """
        # Supprimer un menu spécifique par ID
        self.cursor.execute('DELETE FROM menu WHERE id = ?', (id,))
        self.conn.commit()
        return 'Suppression réussie'

    def update(self):
        """
        Met à jour les informations du menu actuel dans la base de données.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si le menu existe déjà
        menu = self.get_by_id(self.id)
        menu2 = self.get_by_champ("nom", self.nom)
        print(self.id)
        print(menu2)
        try:
            if menu2[0][0] != self.id:
                return 'Un menu avec ce nom existe déjà!!!'
            else:
                if len(menu) > 0:
                    self.cursor.execute('UPDATE menu SET nom = ?, description = ?, prix = ? WHERE id = ?', 
                                        (self.nom, self.description, self.prix, self.id))
                    self.conn.commit()
                    return 'Mise à jour réussie'
                else:
                    return "Le menu n'existe pas!!!"
        except:
            if len(menu) > 0:
                self.cursor.execute('UPDATE menu SET nom = ?, description = ?, prix = ? WHERE id = ?', 
                                    (self.nom, self.description, self.prix, self.id))
                self.conn.commit()
                return 'Mise à jour réussie'
            else:
                return "Le menu n'existe pas!!!"
    
    def update_by_id(self, id, nom, description, prix):
        """
        Met à jour un menu spécifique par son ID.

        Args:
            id (int): Identifiant du menu.
            nom (str): Nom du menu.
            description (str): Description du menu.
            prix (float): Prix du menu.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si le menu existe déjà
        menu = self.get_by_id(self.id)
        if len(menu) > 0:
            self.cursor.execute('UPDATE menu SET nom = ?, description = ?, prix = ? WHERE id = ?', 
                                (nom, description, prix, id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "Le menu n'existe pas!!!"

    def __del__(self):
        """
        Ferme la connexion à la base de données lors de la suppression de l'objet.
        """
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
