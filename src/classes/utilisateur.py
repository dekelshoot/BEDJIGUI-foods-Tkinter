import sqlite3  # Module pour interagir avec les bases de données SQLite
import shelve   # Module pour la persistance des objets Python


class Utilisateur:
    """
    Représente un utilisateur dans une base de données SQLite.
    """

    # Déclaration des attributs de classe
    id = None
    nom = None
    prenom = None
    nom_d_utilisateur = None
    mot_de_passe = None
    email = None
    telephone = None
    adresse = None
    est_admin = None

    def __init__(self, db_name):
        """
        Initialise une connexion à la base de données SQLite et crée la table si elle n'existe pas.

        Args:
            db_name (str): Le nom de la base de données SQLite.
        """
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table utilisateur si elle n'existe pas déjà
    
    def create_table(self):
        """
        Crée la table 'utilisateur' dans la base de données si elle n'existe pas déjà.
        """
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INTEGER PRIMARY KEY, 
            nom TEXT, 
            prenom TEXT, 
            nom_d_utilisateur TEXT, 
            mot_de_passe TEXT,
            email TEXT, 
            telephone TEXT, 
            est_admin INTEGER,
            adresse TEXT);
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, nom, prenom, nom_d_utilisateur, mot_de_passe, email, telephone, adresse):
        """
        Ajoute les informations de l'utilisateur aux attributs de l'objet.

        Args:
            nom (str): Le nom de l'utilisateur.
            prenom (str): Le prénom de l'utilisateur.
            nom_d_utilisateur (str): Le nom d'utilisateur.
            mot_de_passe (str): Le mot de passe de l'utilisateur.
            email (str): L'email de l'utilisateur.
            telephone (str): Le numéro de téléphone de l'utilisateur.
            adresse (str): L'adresse de l'utilisateur.
        """
        self.nom = nom
        self.prenom = prenom
        self.nom_d_utilisateur = nom_d_utilisateur
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.mot_de_passe = mot_de_passe

    def register(self):
        """
        Enregistre un nouvel utilisateur dans la base de données.

        Returns:
            str: Message indiquant que le compte a été créé ou que l'utilisateur existe déjà.
        """
        # Vérifier si l'utilisateur existe déjà
        usr = self.get_by_champ("nom_d_utilisateur", self.nom_d_utilisateur)
        if len(usr) > 0:
            return "l'utilisateur existe déjà"

        # Ajouter l'utilisateur à la base de données
        data = self.get_all()
        self.est_admin = 1 if len(data) == 0 else 0  # Premier utilisateur est admin
        self.cursor.execute('INSERT INTO utilisateur (nom, prenom, nom_d_utilisateur, mot_de_passe, email, telephone, est_admin, adresse) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                            (self.nom, self.prenom, self.nom_d_utilisateur, self.mot_de_passe, self.email, self.telephone, self.est_admin, self.adresse))
        self.conn.commit()  # Valider la transaction

        # Récupérer l'utilisateur pour obtenir son ID
        usr = self.get_by_champ("nom_d_utilisateur", self.nom_d_utilisateur)
        self.id = usr[0][0]

        # Stocker les informations de l'utilisateur dans shelve
        with shelve.open('utilisateur') as user:
            user['id'] = self.id
            user['nom'] = self.nom
            user['prenom'] = self.prenom
            user['email'] = self.email
            user['telephone'] = self.telephone
            user['nom_d_utilisateur'] = self.nom_d_utilisateur
            user['adresse'] = self.adresse
            user['est_admin'] = self.est_admin
        return "Le compte a été créé"

    def get(self):
        """
        Récupère les informations de l'utilisateur par ID.

        Returns:
            list: Informations de l'utilisateur.
        """
        query = 'SELECT * FROM utilisateur WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        """
        Récupère un utilisateur spécifique par ID.

        Args:
            id (int): L'identifiant de l'utilisateur.

        Returns:
            list: Informations de l'utilisateur.
        """
        query = 'SELECT * FROM utilisateur WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        """
        Récupère les utilisateurs par un champ spécifique.

        Args:
            champ (str): Le champ à rechercher.
            value (str): La valeur du champ.

        Returns:
            list: Informations des utilisateurs correspondant au champ.
        """
        query = f'SELECT * FROM utilisateur WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        """
        Récupère tous les utilisateurs.

        Returns:
            list: Informations de tous les utilisateurs.
        """
        self.cursor.execute('SELECT * FROM utilisateur')
        return self.cursor.fetchall()

    def delete(self):
        """
        Supprime l'utilisateur par ID.
        """
        self.cursor.execute('DELETE FROM utilisateur WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        """
        Supprime un utilisateur spécifique par ID.

        Args:
            id (int): L'identifiant de l'utilisateur.
        """
        self.cursor.execute('DELETE FROM utilisateur WHERE id = ?', (id,))
        self.conn.commit()

    def login(self, nom_d_utilisateur, mot_de_passe):
        """
        Vérifie les informations de connexion et connecte l'utilisateur.

        Args:
            nom_d_utilisateur (str): Le nom d'utilisateur.
            mot_de_passe (str): Le mot de passe.

        Returns:
            str: Message indiquant le résultat de la connexion.
        """
        usr = self.get_by_champ("nom_d_utilisateur", nom_d_utilisateur)
        if len(usr) == 0:
            return "aucun utilisateur correspondant"
        if usr[0][4] == mot_de_passe:
            with shelve.open('utilisateur') as user:
                user['id'] = usr[0][0]
                user['nom'] = usr[0][1]
                user['prenom'] = usr[0][2]
                user['nom_d_utilisateur'] = usr[0][3]
                user['email'] = usr[0][5]
                user['telephone'] = usr[0][6]
                user['est_admin'] = usr[0][7]
            return "connexion réussie"
        return "le mot de passe ou le nom d'utilisateur ne correspond pas"

    def __del__(self):
        """
        Ferme la connexion à la base de données lors de la suppression de l'objet.
        """
        self.conn.close()
