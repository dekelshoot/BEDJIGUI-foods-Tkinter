# Import de la classe AccueilWindow depuis le module composants.accueil_window
from composants.accueil_window import AccueilWindow

# Vérification si le script est exécuté en tant que programme principal
if __name__ == "__main__":
    # Création d'une instance de la classe AccueilWindow
    app = AccueilWindow()
    # Lancement de la boucle principale de l'interface utilisateur
    app.mainloop()