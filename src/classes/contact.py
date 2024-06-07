import sqlite3  # Module pour interagir avec les bases de données SQLite


class Contact:
    """
    Classe représentant un contact dans une base de données.
    """

    # Déclaration des attributs de classe
    id = None
    id_utilisateur = None
    sujet = None
    message = None
    date = None

    def __init__(self, db_name):
        """
        Initialise une nouvelle instance de la classe Contact.

        Args:
            db_name (str): Nom de la base de données SQLite.
        """
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table contact si elle n'existe pas déjà
    
    def create_table(self):
        """
        Crée la table contact dans la base de données si elle n'existe pas déjà.
        """
        # Création de la table contact
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY, 
            id_utilisateur INTEGER,
            sujet TEXT,
            message TEXT,
            date TEXT,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, id_utilisateur, sujet, message, date, id=None):
        """
        Ajoute les informations du contact aux attributs de l'objet.

        Args:
            id_utilisateur (int): Identifiant de l'utilisateur.
            sujet (str): Sujet du contact.
            message (str): Message du contact.
            date (str): Date du contact.
            id (int, optional): Identifiant du contact. Défaut à None.
        """
        # Ajouter les informations du contact aux attributs de l'objet
        self.id_utilisateur = id_utilisateur
        self.sujet = sujet
        self.date = date
        self.message = message
        if id is not None:
            self.id = id

    def save(self):
        """
        Enregistre le contact dans la base de données.

        Returns:
            str: Message indiquant que le contact a été ajouté.
        """
        # Ajouter le contact à la base de données
        self.cursor.execute('INSERT INTO contact (id_utilisateur, sujet, message, date) VALUES (?, ?, ?, ?)', 
                            (self.id_utilisateur, self.sujet, self.message, self.date))
        self.conn.commit()  # Valider la transaction
        self.id = self.cursor.lastrowid  # Récupérer l'identifiant du contact ajouté

        return 'Le contact a été ajouté'

    def get(self):
        """
        Récupère les informations du contact actuel depuis la base de données.

        Returns:
            list: Informations du contact.
        """
        # Récupérer les informations du contact
        query = 'SELECT * FROM contact WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        """
        Récupère un contact spécifique par son ID.

        Args:
            id (int): Identifiant du contact.

        Returns:
            list: Informations du contact.
        """
        # Récupérer un contact spécifique par ID
        query = 'SELECT * FROM contact WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        """
        Récupère les contacts par un champ spécifique.

        Args:
            champ (str): Nom du champ.
            value (any): Valeur du champ.

        Returns:
            list: Liste des contacts correspondant au champ et à la valeur spécifiés.
        """
        # Récupérer les contacts par un champ spécifique
        query = f'SELECT * FROM contact WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        """
        Récupère tous les contacts de la base de données.

        Returns:
            list: Liste de tous les contacts.
        """
        # Récupérer tous les contacts
        self.cursor.execute('SELECT * FROM contact')
        return self.cursor.fetchall()

    def delete(self):
        """
        Supprime le contact actuel de la base de données.
        """
        # Supprimer le contact
        self.cursor.execute('DELETE FROM contact WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        """
        Supprime un contact spécifique par son ID.

        Args:
            id (int): Identifiant du contact à supprimer.

        Returns:
            str: Message indiquant que la suppression a été réussie.
        """
        # Supprimer un contact spécifique par ID
        self.cursor.execute('DELETE FROM contact WHERE id = ?', (id,))
        self.conn.commit()
        return 'Suppression réussie'

    def update(self):
        """
        Met à jour les informations du contact actuel dans la base de données.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si le contact existe déjà
        contact = self.get_by_id(self.id)
        if len(contact) > 0:
            self.cursor.execute('UPDATE contact SET id_utilisateur = ?, sujet = ?, message = ?, date = ? WHERE id = ?', 
                                (self.id_utilisateur, self.sujet, self.message, self.date, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "Le contact n'existe pas!!!"
    
    def update_by_id(self, id, id_utilisateur, sujet, message, date):
        """
        Met à jour un contact spécifique par son ID.

        Args:
            id (int): Identifiant du contact.
            id_utilisateur (int): Identifiant de l'utilisateur.
            sujet (str): Sujet du contact.
            message (str): Message du contact.
            date (str): Date du contact.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si le contact existe déjà
        contact = self.get_by_id(id)
        if len(contact) > 0:
            self.cursor.execute('UPDATE contact SET id_utilisateur = ?, sujet = ?, message = ?, date = ? WHERE id = ?', 
                                (id_utilisateur, sujet, message, date, id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "Le contact n'existe pas!!!"
    
    def __del__(self):
        """
        Ferme la connexion à la base de données lors de la suppression de l'objet.
        """
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
