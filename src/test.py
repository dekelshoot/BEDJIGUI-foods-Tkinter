from classes.utilisateur import Utilisateur
import shelve
a=Utilisateur("restaurant.db")
a.add("dekel","shoot","dekelshoot","dekel693","juniortchoupe5@gmail.com","+237693034689","yaoundé")
print(a.register())

with shelve.open('utilisateur') as db:
    # Récupération des données
    id='id'
    if id in db:
        print("vraie")
    else:
        print("faux")
        print(db["id"])

# print(a.login("dekelshoot","dekel693"))