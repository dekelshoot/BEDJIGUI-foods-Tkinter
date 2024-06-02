import sqlite3  # Module pour interagir avec les bases de données SQLite


class Reservation:
    # Déclaration des attributs de classe
    id = None
    id_utilisateur = None
    nombre_personne= None
    heure = None
    date = None
    statut = None
    commentaire = None

    

    def __init__(self, db_name):
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la reservation reservation si elle n'existe pas déjà
    
    def create_table(self):
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

    def add(self, id_utilisateur, nombre_personne,heure,date,statut,commentaire,id=None):
        # Ajouter les informations de l'reservation aux attributs de l'objet
        self.id_utilisateur = id_utilisateur
        self.nombre_personne = nombre_personne
        self.heure = heure
        self.date = date
        self.statut = statut
        self.commentaire = commentaire
        if id != None: self.id = id
        

    def save(self):
        # Ajouter le reservation à la base de données

        self.cursor.execute('INSERT INTO reservation ( id_utilisateur, nombre_personne,heure,date,statut,commentaire) VALUES (?, ?, ?, ?, ?, ?)', 
                            ( self.id_utilisateur, self.nombre_personne,self.heure,self.date,self.statut,self.commentaire))
        self.conn.commit()  # Valider la transaction

        return 'La reservation a été éffectuée'

    def get(self):
        # Récupérer les informations du reservation 
        query = 'SELECT * FROM reservation WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        # Récupérer un reservation spécifique par ID
        query = 'SELECT * FROM reservation WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        # Récupérer les reservations par un champ spécifique (nom du reservation, prix, etc.)
        query = f'SELECT * FROM reservation WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        # Récupérer tous les reservations
        self.cursor.execute('SELECT * FROM reservation')
        return self.cursor.fetchall()

    def delete(self):
        # Supprimer le reservation 
        self.cursor.execute('DELETE FROM reservation WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        # Supprimer un reservation spécifique par ID
        self.cursor.execute('DELETE FROM reservation WHERE id = ?', (id,))
        self.conn.commit()
        return 'suppréssion réussie '

    def update(self):
        # Vérifier si le reservation existe déjà
        reservation = self.get_by_id(self.id)
        if len(reservation) > 0:
            self.cursor.execute('UPDATE reservation SET id_utilisateur = ?, nombre_personne = ?, heure = ?, date = ? , statut = ? , commentaire = ? WHERE id = ?', (self.id_utilisateur, self.nombre_personne,self.heure,self.date,self.statut,self.commentaire, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "le reservation n'existe pas!!!"

        
    
        

    def update_by_id(self, id, id_utilisateur, nombre_personne,heure,date,statut,commentaire):
        # Vérifier si le reservation existe déjà
        reservation = self.get_by_id(self.id)
        if len(reservation) > 0:
            self.cursor.execute('UPDATE reservation SET id_utilisateur = ?, nombre_personne = ?, heure = ?, date = ? , statut = ? , commentaire = ? WHERE id = ?', (id_utilisateur, nombre_personne,heure,date,statut,commentaire, id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "le reservation n'existe pas!!!"
    
    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
