# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response, redirect
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .resources import  *
from .utils import *
import os
import datetime
import jwt
import json


app = Flask(__name__)
api = Api(app)

# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')
# To get one variable, tape app.config['MY_VARIABLE']


# def save_data(data, filename=file_data):
    # """"Enregistre les nouvelles données dans notre fichier de données"""
    # with open(os.path.join("data", filename), "w", encoding="utf8") as data_file:
        # for place in data:
            # data_file.write(place['geonameid']+"\t"+place['name']+"\t"+place['asciiname']+"\t"+place['alternatenames']+"\t"+place['latitude']+"\t"+place['longitude']+"\t"+place['feature class']+"\t"+place['feature code']+"\t"+place['country code']+"\t"+place['cc2']+"\t"+place['admin1 code']+"\t"+place['admin2 code']+"\t"+place['admin3 code']+"\t"+place['admin4 code']+"\t"+place['population']+"\t"+place['elevation']+"\t"+place['dem']+"\t"+place['timezone']+"\t"+place['modification date']+"\n")


#=========================================================================



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
