import sqlite3  # Module pour interagir avec les bases de données SQLite


class Contact:
    # Déclaration des attributs de classe
    id = None
    id_utilisateur = None
    sujet = None
    message = None
    date = None
    

    def __init__(self, db_name):
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table contact si elle n'existe pas déjà
    
    def create_table(self):
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

    def add(self, id_utilisateur, sujet, message, date ,id=None):
        # Ajouter les informations de l'contact aux attributs de l'objet
        self.id_utilisateur = id_utilisateur
        self.sujet = sujet
        self.date= date
        self.message = message
        if id != None: self.id = id
        

    def save(self):
        # Ajouter le contact à la base de données

        self.cursor.execute('INSERT INTO contact (id_utilisateur, sujet, message, date) VALUES (?, ?, ?, ?)', 
                            (self.id_utilisateur, self.sujet, self.message, self.date))
        self.conn.commit()  # Valider la transaction
        self.id = self.cursor.lastrowid 

        return 'Le contact a été ajouté'

    def get(self):
        # Récupérer les informations du contact 
        query = 'SELECT * FROM contact WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        # Récupérer un contact spécifique par ID
        query = 'SELECT * FROM contact WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        # Récupérer les contacts par un champ spécifique (id_utilisateur du contact, message, etc.)
        query = f'SELECT * FROM contact WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        # Récupérer tous les contacts
        self.cursor.execute('SELECT * FROM contact')
        return self.cursor.fetchall()

    def delete(self):
        # Supprimer le contact 
        self.cursor.execute('DELETE FROM contact WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        # Supprimer un contact spécifique par ID
        self.cursor.execute('DELETE FROM contact WHERE id = ?', (id,))
        self.conn.commit()
        return 'suppréssion réussie '

    def update(self):
        # Vérifier si le contact existe déjà
        contact = self.get_by_id(self.id)
        if len(contact) > 0:
            self.cursor.execute('UPDATE contact SET  id_utilisateur = ?, sujet = ?, message = ?, date = ? WHERE id = ?', (self.id_utilisateur,self.sujet,self.message,self.date, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "la contact n'existe pas!!!"
        
    
        

    def update_by_id(self, id, id_utilisateur, sujet, message,date):
        # Vérifier si le contact existe déjà
        contact = self.get_by_id(self.id)
        if len(contact) > 0:
            self.cursor.execute('UPDATE contact SET  id_utilisateur = ?, sujet = ?, message = ?, date = ? WHERE id = ?', (id_utilisateur,sujet,message,date, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "la contact n'existe pas!!!"
    

    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
