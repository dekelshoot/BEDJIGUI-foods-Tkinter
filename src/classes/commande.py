import sqlite3  # Module pour interagir avec les bases de données SQLite


class Commande:
    # Déclaration des attributs de classe
    id = None
    id_utilisateur = None
    status = None
    date = None

    

    def __init__(self, db_name):
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table commande si elle n'existe pas déjà
    
    def create_table(self):
        # Création de la table commande
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS commande (
            id INTEGER PRIMARY KEY, 
            id_utilisateur INTEGER,
            statut TEXT,
            date TEXT,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id));
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self,id_utilisateur,statut,date,id=None):
        # Ajouter les informations de la commande aux attributs de l'objet

        self.statut = statut
        self.date = date
        self.id_utilisateur = id_utilisateur
        if id != None: self.id = id
        

    def save(self):
        # Ajouter la commande à la base de données
        self.cursor.execute('INSERT INTO commande (id_utilisateur,statut,date) VALUES ( ?, ?, ?)', 
                            (self.id_utilisateur,self.statut,self.date))
        self.conn.commit()  # Valider la transaction
        self.id = self.cursor.lastrowid 

        return 'La commande a été ajouté'

    def get(self):
        # Récupérer les informations d'une commande 
        query = 'SELECT * FROM commande WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        # Récupérer une commande spécifique par ID
        query = 'SELECT * FROM commande WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        # Récupérer les commandes par un champ spécifique (nom du commande, prix, etc.)
        query = f'SELECT * FROM commande WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()
    
    def get_by_2_champ(self, champ1,champ2, value1,value2):
        # Récupérer les commandes par un champ spécifique (nom du commande, prix, etc.)
        query = f'SELECT * FROM commande WHERE {champ1} = ? AND {champ2} = ?'
        self.cursor.execute(query, (value1,value2))
        return self.cursor.fetchall()

    def get_all(self):
        # Récupérer tous les commandes
        self.cursor.execute('SELECT * FROM commande')
        return self.cursor.fetchall()

    def delete(self):
        # Supprimer le commande 
        self.cursor.execute('DELETE FROM commande WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        # Supprimer un commande spécifique par ID
        self.cursor.execute('DELETE FROM commande WHERE id = ?', (id,))
        self.conn.commit()
        return 'la commande à été annulé '

    def update(self):
        # Vérifier si le commande existe déjà
        commande = self.get_by_id(self.id)
        if len(commande) > 0:
            self.cursor.execute('UPDATE commande SET  id_utilisateur = ?, statut = ?, date = ? WHERE id = ?', (self.id_utilisateur,self.statut,self.date, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "la commande n'existe pas!!!"

            
    

    def update_by_id(self,id_utilisateur,total,statut,date, ):
        # Vérifier si le commande existe déjà
        commande = self.get_by_id(self.id)
        if len(commande) > 0:
            self.cursor.execute('UPDATE commande SET  id_utilisateur = ?, statut = ?, date = ? WHERE id = ?', (id_utilisateur,statut,date, self.id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "la commande n'existe pas!!!"
    
    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
