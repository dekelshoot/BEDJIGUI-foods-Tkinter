import sqlite3  # Module pour interagir avec les bases de données SQLite


class Menu:
    # Déclaration des attributs de classe
    id = None
    nom = None
    description = None
    prix = None
    

    def __init__(self, db_name):
        # Connexion à la base de données SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()  # Créer la table menu si elle n'existe pas déjà
    
    def create_table(self):
        # Création de la table menu
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY, 
                nom TEXT, 
                description TEXT, 
                prix REAL);
        ''')
        self.conn.commit()  # Valider la transaction

    def add(self, nom, description, prix,id=None):
        # Ajouter les informations de l'menu aux attributs de l'objet
        self.nom = nom
        self.description = description
        self.prix = prix
        if id != None: self.id = id
        

    def save(self):
        # Vérifier si le menu existe déjà
        menu = self.get_by_champ("nom", self.nom)
        if len(menu) > 0:
            return 'le menu existe déjà'
        # Ajouter le menu à la base de données

        self.cursor.execute('INSERT INTO menu (nom, description, prix) VALUES (?, ?, ?)', 
                            (self.nom, self.description, self.prix))
        self.conn.commit()  # Valider la transaction

        # Récupérer le menu pour obtenir son ID
        menu = self.get_by_champ("nom", self.nom)
        self.id = menu[0][0]

        return 'Le menu a été ajouté'

    def get(self):
        # Récupérer les informations du menu 
        query = 'SELECT * FROM menu WHERE id = ?'
        self.cursor.execute(query, (self.id,))
        return self.cursor.fetchall()

    def get_by_id(self, id):
        # Récupérer un menu spécifique par ID
        query = 'SELECT * FROM menu WHERE id = ?'
        self.cursor.execute(query, (id,))
        return self.cursor.fetchall()
    
    def get_by_champ(self, champ, value):
        # Récupérer les menus par un champ spécifique (nom du menu, prix, etc.)
        query = f'SELECT * FROM menu WHERE {champ} = ?'
        self.cursor.execute(query, (value,))
        return self.cursor.fetchall()

    def get_all(self):
        # Récupérer tous les menus
        self.cursor.execute('SELECT * FROM menu')
        return self.cursor.fetchall()

    def delete(self):
        # Supprimer le menu 
        self.cursor.execute('DELETE FROM menu WHERE id = ?', (self.id,))
        self.conn.commit()

    def delete_by_id(self, id):
        # Supprimer un menu spécifique par ID
        self.cursor.execute('DELETE FROM menu WHERE id = ?', (id,))
        self.conn.commit()
        return 'suppréssion réussie '

    def update(self):
        # Vérifier si le menu existe déjà
        menu = self.get_by_id(self.id)
        menu2 = self.get_by_champ("nom",self.nom)
        print(self.id)
        print(menu2)
        try:
            if menu2[0][0]!=self.id:
                return 'Un menu avec ce nom existe déja!!!'
            else:
                if len(menu) > 0:
                    self.cursor.execute('UPDATE menu SET nom = ?, description = ?, prix = ? WHERE id = ?', (self.nom, self.description, self.prix, self.id))
                    self.conn.commit()
                    return 'Mise à jour réussie'
                else:
                    return "le menu n'existe pas!!!"
        except:
            if len(menu) > 0:
                self.cursor.execute('UPDATE menu SET nom = ?, description = ?, prix = ? WHERE id = ?', (self.nom, self.description, self.prix, self.id))
                self.conn.commit()
                return 'Mise à jour réussie'
            else:
                return "le menu n'existe pas!!!"
        
    
        

    def update_by_id(self, id, nom, description, prix):
        # Vérifier si le menu existe déjà
        menu = self.get_by_id(self.id)
        if len(menu) > 0:
            self.cursor.execute('UPDATE menu SET nom = ?, description = ?, prix = ? WHERE id = ?', (nom, description, prix, id))
            self.conn.commit()
            return 'Mise à jour réussie'
        else:
            return "le menu n'existe pas!!!"
    

    def __del__(self):
        # Fermer la connexion à la base de données lors de la suppression de l'objet
        self.conn.close()
