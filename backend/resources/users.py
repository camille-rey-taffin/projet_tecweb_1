# coding: utf-8

import os
import json

class User:
    "Réprésente un utilisateur avec ses informations"

    def __init__(self, id:str, nom:str, prenom:str, fonction:str, anciennete:int, mise_a_jour:str, conge:int, actif:bool, actionnaire:bool, missions:list):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.fonction = fonction
        self.anciennete = anciennete
        self.mise_a_jour = mise_a_jour
        self.conge = conge
        self.actif = actif
        self.actionnaire = actionnaire
        self.missions = missions

    def to_json(self):
        '''Renvoie les informations de l'utilisateur au format json'''
        return {
            "id" : self.id,
            "nom" : self.nom,
            "prenom" : self.prenom,
            "fonction" : self.fonction,
            "anciennete" : self.anciennete,
            "mise_a_jour" : self.mise_a_jour,
            "conge" : self.conge,
            "actif" : self.actif,
            "actionnaire" : self.actionnaire,
            "missions" : self.missions
            }

def get_users(filename="users.json"):
    """Crée la liste des utilisateurs"""

    with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
        accounts = json.load(data_file)
    users = []
    for num, account in accounts.items():
        user = User(**account)
        users.append(user)
    return users

# création de la liste des utilisateurs
users = get_users()

def verify_user(nom:str, prenom:str):
    """Vérifie que l'utilisateur est autorisé"""
    for user in users:
        if user.nom == nom and user.prenom == prenom:
            return user
    raise ValueError
