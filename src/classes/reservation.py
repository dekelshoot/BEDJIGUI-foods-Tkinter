import sqlite3  # Module pour interagir avec les bases de données SQLite


class Reservation:
    """
    Classe représentant une réservation dans une base de données.
    """

    # Déclaration des attributs de classe
    id = None
    id_utilisateur = None
    nombre_personne = None
    heure = None
    date = None
    statut = None
    commentaire = None

    def __init__(self, db_name):
        """
        Initialise une nouvelle instance de la classe Reservation.

        Args:
            db_name (str): Nom de la base de données SQLite.
        """
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table reservation si elle n'existe pas déjà
    
    def create_table(self):
        """
        Crée la table reservation dans la base de données si elle n'existe pas déjà.
        """
        # Création de la table reservation
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservation (
            id INTEGER PRIMARY KEY, 
            id_utilisateur INTEGER,
            nombre_personne INTEGER,
            heure TEXT,
            date TEXT,
            statut TEXT, 
            commentaire TEXT, 
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, id_utilisateur, nombre_personne, heure, date, statut, commentaire, id=None):
        """
        Ajoute les informations de la réservation aux attributs de l'objet.

        Args:
            id_utilisateur (int): Identifiant de l'utilisateur.
            nombre_personne (int): Nombre de personnes pour la réservation.
            heure (str): Heure de la réservation.
            date (str): Date de la réservation.
            statut (str): Statut de la réservation.
            commentaire (str): Commentaire pour la réservation.
            id (int, optional): Identifiant de la réservation. Défaut à None.
        """
        self.id_utilisateur = id_utilisateur
        self.nombre_personne = nombre_personne
        self.heure = heure
        self.date = date
        self.statut = statut
        self.commentaire = commentaire
        if id is not None:
            self.id = id

    def save(self):
        """
        Enregistre la réservation dans la base de données.

        Returns:
            str: Message indiquant que la réservation a été effectuée.
        """
        # Ajouter la réservation à la base de données
        self.cursor.execute('INSERT INTO reservation (id_utilisateur, nombre_personne, heure, date, statut, commentaire) VALUES (?, ?, ?, ?, ?, ?)', 
                            (self.id_utilisateur, self.nombre_personne, self.heure, self.date, self.statut, self.commentaire))
        self.conn.commit()  # Valider la transaction

        return 'La réservation a été effectuée'

    def get(self):
        """
        Récupère les informations de la réservation actuelle depuis la base de données.

        Returns:
            list: Informations de la réservation.
        """
        # Récupérer les informations de la réservation
        query = 'SELECT * FROM reservation WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        """
        Récupère une réservation spécifique par son ID.

        Args:
            id (int): Identifiant de la réservation.

        Returns:
            list: Informations de la réservation.
        """
        # Récupérer une réservation spécifique par ID
        query = 'SELECT * FROM reservation WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        """
        Récupère les réservations par un champ spécifique.

        Args:
            champ (str): Nom du champ.
            value (any): Valeur du champ.

        Returns:
            list: Liste des réservations correspondant au champ et à la valeur spécifiés.
        """
        # Récupérer les réservations par un champ spécifique
        query = f'SELECT * FROM reservation WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        """
        Récupère toutes les réservations de la base de données.

        Returns:
            list: Liste de toutes les réservations.
        """
        # Récupérer toutes les réservations
        self.cursor.execute('SELECT * FROM reservation')
        return self.cursor.fetchall()

    def delete(self):
        """
        Supprime la réservation actuelle de la base de données.
        """
        # Supprimer la réservation
        self.cursor.execute('DELETE FROM reservation WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        """
        Supprime une réservation spécifique par son ID.

        Args:
            id (int): Identifiant de la réservation à supprimer.

        Returns:
            str: Message indiquant que la suppression a été réussie.
        """
        # Supprimer une réservation spécifique par ID
        self.cursor.execute('DELETE FROM reservation WHERE id = ?', (id,))
        self.conn.commit()
        return 'Suppression réussie'

    def update(self):
        """
        Met à jour les informations de la réservation actuelle dans la base de données.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si la réservation existe déjà
        reservation = self.get_by_id(self.id)
        if len(reservation) > 0:
            self.cursor.execute('UPDATE reservation SET id_utilisateur = ?, nombre_personne = ?, heure = ?, date = ?, statut = ?, commentaire = ? WHERE id = ?', 
                                (self.id_utilisateur, self.nombre_personne, self.heure, self.date, self.statut, self.commentaire, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "La réservation n'existe pas!!!"

    def update_by_id(self, id, id_utilisateur, nombre_personne, heure, date, statut, commentaire):
        """
        Met à jour une réservation spécifique par son ID.

        Args:
            id (int): Identifiant de la réservation.
            id_utilisateur (int): Identifiant de l'utilisateur.
            nombre_personne (int): Nombre de personnes pour la réservation.
            heure (str): Heure de la réservation.
            date (str): Date de la réservation.
            statut (str): Statut de la réservation.
            commentaire (str): Commentaire pour la réservation.

        Returns:
            str: Message indiquant le résultat de la mise à jour.
        """
        # Vérifier si la réservation existe déjà
        reservation = self.get_by_id(self.id)
        if len(reservation) > 0:
            self.cursor.execute('UPDATE reservation SET id_utilisateur = ?, nombre_personne = ?, heure = ?, date = ?, statut = ?, commentaire = ? WHERE id = ?', 
                                (id_utilisateur, nombre_personne, heure, date, statut, commentaire, id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "La réservation n'existe pas!!!"
    
    def __del__(self):
        """
        Ferme la connexion à la base de données lors de la suppression de l'objet.
        """
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()