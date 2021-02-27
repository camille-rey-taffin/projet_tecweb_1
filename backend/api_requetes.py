# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response, redirect
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
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
from backend.models import db, Content


class Data(Resource):
    """Gère la manipulation des données"""

    @token_required
    def get(self, current_user, geonameid=None):
        """Gère l'accès et le filtrage des données"""

        # Renvoie toutes les données
        if geonameid==None:
            resp = jsonify({'data': [element.serialize() for element in Content.query.all()]})
            resp.status_code = 200
            return resp

        # Renvoie les données filtrées sur l'asciiname
        # Si aucune donnée n'est trouvée une erreur est renvoyée
        else:
            data = Content.query.filter_by(geonameid=geonameid).first()
            if not data:
                resp = jsonify({'status':'fail', 'message': 'geonameid not found'})
                resp.status_code = 404
                return resp
            else :
                resp = jsonify({'data': data.serialize()})
                resp.status_code = 200
                return resp

    def put(self):
        """Ajoute des données"""

        # On reçoit les informations à ajouter
        # envoyées par l'utilisateur
        data_add = request.json

        # on vérifie qu'un geonameid est bien précisé dans les paramètres
        if "geonameid" not in data_add :
            resp = jsonify({'status': 'fail', 'message' : "geoname id is required for new element"})
            resp.status_code = 400
            return resp

        # On suppose que le geonameid est unique,
        # on l'utilise donc pour identifier les éléments
        # Si le geonameid existe déjà on renvoie une erreur,
        # sinon on peut ajouter les nouvelles données
        element_exists =  Content.query.filter_by(geonameid=data_add["geonameid"]).first()
        if element_exists:
            resp = jsonify({'status': 'fail', 'message' : data_add["geonameid"]+" existe déjà"})
            resp.status_code = 409
            return resp
        else:
            time = datetime.date.today()
            data_add["modification_date"] = str(time)
            try :
                new_data = Content(**data_add)
                db.session.add(new_data)
                db.session.commit()

            except (sqlalchemy.exc.InvalidRequestError, TypeError) as e :
                resp = jsonify({'status': 'fail', 'message' : "wrong format (field doest not exist in db)"})
                resp.status_code = 400
                return resp

            resp = jsonify({'status': 'success', 'message' : "new data "+data_add["geonameid"]+" successfully added"})
            resp.status_code = 200
            return resp


    @token_required
    def post(self, current_user):
        """Modifie"""

        # On reçoit les informations à modifier
        # envoyées par l'utilisateur
        data_modify = request.json

        # on vérifie qu'un geonameid est bien précisé dans les paramètres
        if "geonameid" not in data_modify :
            resp = jsonify({'status': 'fail', 'message' : "geoname of data to modify is required"})
            resp.status_code = 400
            return resp

        geonameid = data_modify["geonameid"]
        # On suppose que le geonameid est unique,
        # on l'utilise donc pour identifier les éléments
        # Si le geonameid n'existe pas on renvoie une erreur,
        # sinon on peut modifier les données
        element =  Content.query.filter_by(geonameid = geonameid)
        element_exists = element.first()

        if not element_exists:
            resp = jsonify({'status': 'fail', 'message' : geonameid +" does not exist in database"})
            resp.status_code = 404
            return resp
        else:
            try :
                element.update(data_modify)
                db.session.commit()
            except sqlalchemy.exc.InvalidRequestError as e :
                resp = jsonify({'status': 'fail', 'message' : "wrong format (field doest not exist in db)"})
                resp.status_code = 400
                return resp


            resp = jsonify({'status': 'success', 'message' : geonameid +" successfully modified"})
            resp.status_code = 200
            return resp

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

class DataSearch(Resource):
    """Gere la recherche d'information"""

    @token_required
    def get(self, current_id):

        params = request.args
        if not params:
            resp = jsonify({'status':'failed', 'message':'missing parameters'})
            resp.status_code = 412
            return resp
        geonameid = params.get('geonameid')
        name = params.get('name')
        asciiname = params.get('asciiname')
        alternatename = params.get('alternatename')
        latitude = params.get('latitude')
        longitude = params.get('longitude')
        country_code = params.get('country_code')

        query_object = Content.query
        if geonameid:
            query_object = query_object.filter_by(geonameid=geonameid)
        if name:
            query_object = query_object.filter_by(name=name)
        if asciiname:
            query_object = query_object.filter_by(asciiname=asciiname)
        if alternatename:
            pattern = '%'+alternatename+'%'
            query_object = query_object.filter(Content.alternatenames.like(pattern))
        if latitude:
            query_object = query_object.filter_by(latitude=latitude)
        if longitude:
            query_object = query_object.filter_by(longitude=longitude)
        if country_code:
            query_object = query_object.filter_by(country_code=country_code)

        resp = jsonify({'results':[element.serialize() for element in query_object.all()]})
        resp.status_code = 200
        return resp


api.add_resource(Login, "/", "/login")
api.add_resource(Data, "/data", "/data/<geonameid>")
api.add_resource(DataSearch, "/data/search")
