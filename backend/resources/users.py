import os
import json

class User:
    "Un utilisateur avec son id, son nom et son prénom"
    def __init__(self, id:str, nom:str, prenom:str):
        self.id = id
        self.nom = nom
        self.prenom = prenom

    def to_json(self):
        return {
            "id":self.id,
            "nom":self.nom,
            "prenom":self.prenom
            }

def get_users(filename="users.json"):
    """Crée les comptes utilisateur"""
    with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
        accounts = json.load(data_file)
    users = []
    for num, account in accounts.items():
        user = User(account["id"], account["nom"], account["prenom"])
        users.append(user)
    return users

users = get_users()

def verify_user(nom:str, prenom:str):
    """Vérifie que l'utilisateur est autorisé"""
    for user in users:
        if user.nom == nom and user.prenom == prenom:
            return user
    return False
