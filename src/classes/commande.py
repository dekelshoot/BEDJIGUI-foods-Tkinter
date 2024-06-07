import sqlite3  # Module pour interagir avec les bases de données SQLite

class Commande:
    """
    Classe représentant une commande dans une base de données.
    """

    # Déclaration des attributs de classe
    id = None
    id_utilisateur = None
    status = None
    date = None
    commentaire = None

    def __init__(self, db_name):
        """
        Initialise une nouvelle instance de la classe Commande.

        Args:
            db_name (str): Nom de la base de données SQLite.
        """
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table commande si elle n'existe pas déjà
    
    def create_table(self):
        """
        Crée la table commande dans la base de données si elle n'existe pas déjà.
        """
        # Création de la table commande
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS commande (
            id INTEGER PRIMARY KEY, 
            id_utilisateur INTEGER,
            statut TEXT,
            date TEXT,
            commentaire TEXT,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, id_utilisateur, statut, date, commentaire, id=None):
        """
        Ajoute les informations de la commande aux attributs de l'objet.

        Args:
            id_utilisateur (int): Identifiant de l'utilisateur.
            statut (str): Statut de la commande.
            date (str): Date de la commande.
            id (int, optional): Identifiant de la commande. Défaut à None.
        """
        # Ajouter les informations de la commande aux attributs de l'objet
        self.statut = statut
        self.date = date
        self.id_utilisateur = id_utilisateur
        self.commentaire = commentaire
        if id is not None:
            self.id = id

    def save(self):
        """
        Enregistre la commande dans la base de données.

        Returns:
            str: Message indiquant que la commande a été ajoutée.
        """
        # Ajouter la commande à la base de données
        self.cursor.execute('INSERT INTO commande (id_utilisateur, statut, date, commentaire) VALUES (?, ?, ?,?)', 
                            (self.id_utilisateur, self.statut, self.date, self.commentaire))
        self.conn.commit()  # Valider la transaction
        self.id = self.cursor.lastrowid  # Récupérer l'identifiant de la commande ajoutée

        return 'La commande a été ajoutée'

    def get(self):
        """
        Récupère les informations de la commande actuelle depuis la base de données.

        Returns:
            list: Informations de la commande.
        """
        # Récupérer les informations d'une commande
        query = 'SELECT * FROM commande WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        """
        Récupère une commande spécifique par son ID.

        Args:
            id (int): Identifiant de la commande.

        Returns:
            list: Informations de la commande.
        """
        # Récupérer une commande spécifique par ID
        query = 'SELECT * FROM commande WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        """
        Récupère les commandes par un champ spécifique.

        Args:
            champ (str): Nom du champ.
            value (any): Valeur du champ.

        Returns:
            list: Liste des commandes correspondant au champ et à la valeur spécifiés.
        """
        # Récupérer les commandes par un champ spécifique
        query = f'SELECT * FROM commande WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()
    
    def get_by_2_champ(self, champ1, champ2, value1, value2):
        """
        Récupère les commandes par deux champs spécifiques.

        Args:
            champ1 (str): Nom du premier champ.
            champ2 (str): Nom du deuxième champ.
            value1 (any): Valeur du premier champ.
            value2 (any): Valeur du deuxième champ.

        Returns:
            list: Liste des commandes correspondant aux champs et valeurs spécifiés.
        """
        # Récupérer les commandes par deux champs spécifiques
        query = f'SELECT * FROM commande WHERE {champ1} = ? AND {champ2} = ?'
        self.cursor.execute(query, (value1, value2))
        return self.cursor.fetchall()

    def get_all(self):
        """
        Récupère toutes les commandes de la base de données.

        Returns:
            list: Liste de toutes les commandes.
        """
        # Récupérer toutes les commandes
        self.cursor.execute('SELECT * FROM commande')
        return self.cursor.fetchall()

    def delete(self):
        """
        Supprime la commande actuelle de la base de données.
        """
        # Supprimer la commande
        self.cursor.execute('DELETE FROM commande WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        """
        Supprime une commande spécifique par son ID.

        Args:
            id (int): Identifiant de la commande à supprimer.

        Returns:
            str: Message indiquant que la commande a été annulée.
        """
        # Supprimer une commande spécifique par ID
        self.cursor.execute('DELETE FROM commande WHERE id = ?', (id,))
        self.conn.commit()
        return 'La commande a été annulée'

    def update(self):
        """
        Met à jour les informations de la commande actuelle dans la base de données.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si la commande existe déjà
        commande = self.get_by_id(self.id)
        if len(commande) > 0:
            self.cursor.execute('UPDATE commande SET id_utilisateur = ?, statut = ?, date = ?, commentaire = ? WHERE id = ?', 
                                (self.id_utilisateur, self.statut, self.date, self.commentaire, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "La commande n'existe pas!!!"

    def update_by_id(self, id_utilisateur, statut, date ,commentaire):
        """
        Met à jour une commande spécifique par son ID.

        Args:
            id_utilisateur (int): Identifiant de l'utilisateur.
            statut (str): Statut de la commande.
            date (str): Date de la commande.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si la commande existe déjà
        commande = self.get_by_id(self.id)
        if len(commande) > 0:
            self.cursor.execute('UPDATE commande SET id_utilisateur = ?, statut = ?, date = ?, commentaire = ? WHERE id = ?', 
                                (id_utilisateur, statut, date, commentaire, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "La commande n'existe pas!!!"
    
    def __del__(self):
        """
        Ferme la connexion à la base de données lors de la suppression de l'objet.
        """
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
