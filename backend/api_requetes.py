# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response, redirect
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import datetime
import jwt
import json


app = Flask(__name__)
api = Api(app)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
app.config['SECRET_KEY'] = "\xd5PE\xa3t\x96D\xa2\xae\xc2\xcfIq\xe7\xefk"
app.config['tokens_blacklist'] = []
# To get one variable, tape app.config['MY_VARIABLE']

#======================================================================
# Gestion des identifiants des utilisateurs
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


def make_token(user):
    """Crée le token d'authentification"""
    encode_params = {
        "id": user.id,
        "exp": datetime.datetime.utcnow()+\
        datetime.timedelta(minutes=30)
        }
    try:
        token = jwt.encode(encode_params, app.config.get('SECRET_KEY'), algorithm='HS256')
        return token
    except jwt.ExpiredSignatureError:
        return "token expired!"

def verify_user(nom:str, prenom:str):
    """Vérifie que l'utilisateur est autorisé"""
    for user in users:
        if user.nom == nom and user.prenom == prenom:
            return user
        return False

# =====================================================================


def decode_token(token):

    if token in app.config.get('tokens_blacklist'):
            resp = jsonify({'status':'fail', 'message': 'expired token'})
            resp.status_code = 401
            return resp
    else :
        try:
            data = jwt.decode(token, app.config.get('SECRET_KEY'))
            current_user = data["id"]
            return current_user

        except jwt.InvalidTokenError:
            resp = jsonify({'status':'fail', 'message': 'invalid token'})
            resp.status_code = 401
            return resp

        except jwt.ExpiredSignatureError:
            resp = jsonify({'status':'fail', 'message': 'expired token'})
            resp.status_code = 401
            return resp

def token_required(f):
    """Crée le décorateur qui permettra de vérifier la présence
    du token dans le Authorization du header pour chaque requête"""
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        #On vérifie s'il existe un token d'authentification dans le header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            resp = jsonify({'status':'fail', 'message': 'missing token'})
            resp.status_code = 403
            return resp

        #on décode le token
        decoded_token = decode_token(token)
        print(type(decoded_token))
        if not isinstance(decoded_token, str):
            return decoded_token

        else :
            current_user = decoded_token
            return f(current_user, *args, **kwargs)
    return decorator


#========================================================================

# file_data = "FR.txt"
# def get_data(filename=file_data):
    # """Retourne les données contenues dans notre fichier de données"""
    # data = []
    # with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
        # for line in data_file:
            # colonnes = line.strip().split('\t')
            # place = {}
            # place['geonameid'] = colonnes[0]
            # place['name'] = colonnes[1]
            # place['asciiname'] = colonnes[2]
            # place['alternatenames'] = colonnes[3]
            # place['latitude'] = colonnes[4]
            # place['longitude'] = colonnes[5]
            # place['feature class'] = colonnes[6]
            # place['feature code'] = colonnes[7]
            # place['country code'] = colonnes[8]
            # place['cc2'] = colonnes[9]
            # place['admin1 code'] = colonnes[10]
            # place['admin2 code'] = colonnes[11]
            # place['admin3 code'] = colonnes[12]
            # place['admin4 code'] = colonnes[13]
            # place['population'] = colonnes[14]
            # place['elevation'] = colonnes[15]
            # place['dem'] = colonnes[16]
            # place['timezone'] = colonnes[17]
            # place['modification date'] = colonnes[18]
            # data.append(place)
    # return data

# def save_data(data, filename=file_data):
    # """"Enregistre les nouvelles données dans notre fichier de données"""
    # with open(os.path.join("data", filename), "w", encoding="utf8") as data_file:
        # for place in data:
            # data_file.write(place['geonameid']+"\t"+place['name']+"\t"+place['asciiname']+"\t"+place['alternatenames']+"\t"+place['latitude']+"\t"+place['longitude']+"\t"+place['feature class']+"\t"+place['feature code']+"\t"+place['country code']+"\t"+place['cc2']+"\t"+place['admin1 code']+"\t"+place['admin2 code']+"\t"+place['admin3 code']+"\t"+place['admin4 code']+"\t"+place['population']+"\t"+place['elevation']+"\t"+place['dem']+"\t"+place['timezone']+"\t"+place['modification date']+"\n")


#=========================================================================

class Login(Resource):
    """Login"""
    def post(self):
        """"Crée le token d'un utilisateur si les informations reçues
        correspondent bien à un compte utilisateur"""

        # On récupère les informations
        info = request.json

        # On vérifie que les identifiants correpondent à un utilisateur
        # Si oui on crée le token, l'utilisateur correspondant et le token sont renvoyés
        # Si non, une erreur est renvoyé
        user = verify_user(info["name"],info["firstname"])
        if user:
            token = make_token(user)
            return {'User':user.to_json(), 'Token': token.decode('UTF-8')}
        else:
            return {"ERROR":"Nom ou prénom incorrect"}, 400


class Data(Resource):
    """Gère la manipulation des données"""

    @token_required
    def get(self, current_user, geonameid=None):
        """Gère l'accès et le filtrage des données"""

        from backend.models import db, Content
        # Renvoie toutes les données
        if geonameid==None:
            return [element.serialize() for element in Content.query.all()], 200

        # Renvoie les données filtrées sur l'asciiname
        # Si aucune donnée n'est trouvée une erreur est renvoyée
        else:
            if not Content.query.filter_by(geonameid=geonameid):
                res = {"ERROR":"Aucun lieu n'a été trouvé"}, 404
            else :
                return [element.serialize() for element in Content.query.filter_by(geonameid=geonameid)], 200




    # @token_required
    # def put(self, current_user):
        # """Ajoute des données"""

        # On va chercher les données déjà existantes
        # data = get_data()

        # On reçoit les informations à ajouter
        # envoyées par l'utilisateur
        # data_add = request.json

        # On suppose que le geonameid est unique,
        # on l'utilise donc pour identifier les éléments
        # Si le geonameid existe déjà on renvoie une erreur,
        # sinon on peut ajouter les nouvelles données
        # list_id = [d["geonameid"] for d in data]
        # if data_add["geonameid"] in list_id:
            # res = {"ERROR": "geonameid existe déjà"}, 400
            # return res
        # else:
            # time = datetime.date.today()
            # data_add["modification date"] = str(time)
            # data.append(data_add)
            # save_data(data)
            # res = {"OK": "Lieu ajouté avec succès"}, 200
            # return res

    # @token_required
    # def post(self, current_user):
        # """Modifie des données"""

        # On va chercher les données déjà existantes
        # data = get_data()

        # On reçoit les informations à modifier
        # envoyées par l'utilisateur
        # data_edit = request.json

        # On recupère le geonameid pour connaître l'élément à modifier
        # geonameid = request.args.get('geonameid')

        # On cherche l'élément correspondant au geonameid
        # Si on le trouve alors on le modifie avec les informations reçues,
        # Sinon on retourne un erreur
        # for n, d in enumerate(data):
            # if d["geonameid"] == geonameid:
                # for key, value in data_edit.items():
                    # d[key] = value
                # time = datetime.date.today()
                # d["modification date"] = str(time)
                # save_data(data)
                # res = {"OK": "Données modifées avec succès"}, 200
                # return res
        # else :
            # res = {"ERROR": "Lieu non trouvé"}, 404


    # @token_required
    # def delete(self, current_user):
        # """Supprime des données"""

        # On va chercher les données déjà existantes
        # data = get_data()

        # On recupère le geonameid pour connaître l'élément à supprimer
        # geonameid = request.args.get('geonameid')

        # On cherche l'élément correspondant au geonameid
        # Si on le trouve alors on le supprime,
        # Sinon on retourne un erreur
        # for n, d in enumerate(data):
            # if d["geonameid"] == geonameid:
                # del data[n]
                # save_data(data)
                # res = {"OK": "Lieu supprimé avec succés"}, 200
                # return res
        # else:
            # res = {"ERROR": "Lieu non trouvé"}, 404
            # return res


api.add_resource(Login, "/", "/login")
api.add_resource(Data, "/data", "/data/<geonameid>")
