import sqlite3  # Module pour interagir avec les bases de données SQLite
import shelve   # Module pour la persistance des objets Python

class Utilisateur:
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
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table utilisateur si elle n'existe pas déjà
    
    def create_table(self):
        # Création de la table utilisateur
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
        # Ajouter les informations de l'utilisateur aux attributs de l'objet
        self.nom = nom
        self.prenom = prenom
        self.nom_d_utilisateur = nom_d_utilisateur
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.mot_de_passe = mot_de_passe

    def register(self):
        # Vérifier si l'utilisateur existe déjà
        usr = self.get_by_champ("nom_d_utilisateur", self.nom_d_utilisateur)
        if len(usr) > 0:
            return 'l\'utilisateur existe déjà'

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
        return 'Le compte a été créé'

    def get(self):
        # Récupérer les informations de l'utilisateur par ID
        query = 'SELECT * FROM utilisateur WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        # Récupérer un utilisateur spécifique par ID
        query = 'SELECT * FROM utilisateur WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        # Récupérer les utilisateurs par un champ spécifique (nom d'utilisateur, email, etc.)
        query = f'SELECT * FROM utilisateur WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        # Récupérer tous les utilisateurs
        self.cursor.execute('SELECT * FROM utilisateur')
        return self.cursor.fetchall()

    def delete(self):
        # Supprimer l'utilisateur par ID
        self.cursor.execute('DELETE FROM utilisateur WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        # Supprimer un utilisateur spécifique par ID
        self.cursor.execute('DELETE FROM utilisateur WHERE id = ?', (id,))
        self.conn.commit()

    def login(self, nom_d_utilisateur, mot_de_passe):
        # Vérifier les informations de connexion
        usr = self.get_by_champ("nom_d_utilisateur", nom_d_utilisateur)
        if len(usr) == 0:
            return 'aucun utilisateur correspondant'
        if usr[0][4] == mot_de_passe:
            with shelve.open('utilisateur') as user:
                user['id'] = usr[0][0]
                user['nom'] = usr[0][1]
                user['prenom'] = usr[0][2]
                user['nom_d_utilisateur'] = usr[0][3]
                user['email'] = usr[0][5]
                user['telephone'] = usr[0][6]
                user['est_admin'] = usr[0][7]
            return 'connexion réussie'
        return 'le mot de passe ou le nom d\'utilisateur ne correspond pas'

    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
