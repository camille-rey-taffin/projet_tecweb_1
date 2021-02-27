# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy, sqlalchemy

from ..utils import *
from backend.models import db, Content

class Data(Resource):
    """Ressource pourla manipulation des données"""

    @token_required
    def get(self, current_user, geonameid=None):
        """Gère l'accès aux données en lecture"""

        # Renvoie toutes les données
        if geonameid==None:
            resp = jsonify({'data': [element.to_json() for element in Content.query.all()]})
            resp.status_code = 200
            return resp

        # Renvoie les données d'un lieu précis filtré par geonameid
        # Si aucune donnée n'est trouvée une erreur est renvoyée
        else:
            data = Content.query.filter_by(geonameid=geonameid).first()
            if not data:
                resp = jsonify({'status':'fail', 'message': 'geonameid not found'})
                resp.status_code = 404
                return resp
            else :
                resp = jsonify({'data': data.to_json()})
                resp.status_code = 200
                return resp

    @token_required
    def put(self, current_user, geonameid = None):
        """Ajoute des données"""

        # On reçoit les informations à ajouter envoyées dans le body
        data_add = request.json

        # on vérifie qu'un geonameid est bien précisé
        if geonameid == None:
            resp = jsonify({"status" : "fail", "message" : "geonameid to create is missing"})
            resp.status_code = 400
            return resp

        # on vérifie que des données à modifier sont bien précisées (au minimum le champ 'name')
        if not data_add or not data_add.get("name"):
            resp = jsonify({"status" : "failed", "message" : "missing 'name' field of data to create"})
            resp.status_code = 400
            return resp

        # On suppose que le geonameid est unique,
        # on l'utilise donc pour identifier les éléments
        # Si le geonameid existe déjà on renvoie une erreur,
        # sinon on peut ajouter les nouvelles données
        element_exists =  Content.query.filter_by(geonameid = geonameid).first()

        if element_exists:
            resp = jsonify({'status': 'fail', 'message' : geonameid + " existe déjà"})
            resp.status_code = 409
            return resp
        else:
            data_add["geonameid"] = geonameid
            time = datetime.date.today()
            data_add["modification_date"] = str(time)

            try :
                new_data = Content(**data_add)
                db.session.add(new_data)
                db.session.commit()

            # cas ou les données à renseigner ne respectent pas le format de la BDD
            except (sqlalchemy.exc.InvalidRequestError, TypeError) as e :
                resp = jsonify({'status': 'fail', 'message' : "wrong format (field does not exist in db)"})
                resp.status_code = 400
                return resp

            resp = jsonify({'status': 'success', 'message' : "new data "+data_add["geonameid"]+" successfully added"})
            resp.status_code = 200
            return resp

    @token_required
    def post(self, current_user, geonameid = None):
        """Modifie les données d'un lieu"""

        # On reçoit les informations à modifier envoyées dans le body
        data_modify = request.json

        # on vérifie qu'un geonameid est bien précisé
        if geonameid == None:
            resp = jsonify({'status':'fail', 'message': 'geonameid to modify is missing'})
            resp.status_code = 400
            return resp

        # on vérifie que des données à modifier sont bien précisées
        if not data_modify:
            resp = jsonify({'status':'failed', 'message':'missing data to modify'})
            resp.status_code = 400
            return resp

        # on vérifie que l'utilisateur ne cherche pas à modifier un ID (immuable après attribution)
        if data_modify.get('geonameid'):
            resp = jsonify({'status':'failed', 'message':'geonameid cannot be modified'})
            resp.status_code = 400
            return resp

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

            except sqlalchemy.exc.InvalidRequestError:
                resp = jsonify({'status': 'fail', 'message' : "wrong format (field does not exist in db)"})
                resp.status_code = 400
                return resp


            resp = jsonify({'status': 'success', 'message' : geonameid +" successfully modified"})
            resp.status_code = 200
            return resp

    @token_required
    def delete(self, current_user, geonameid = None):
        """Supprime les données d'un lieu précis"""

        # On suppose que le geonameid est unique,
        # on l'utilise donc pour identifier les éléments
        # Si le geonameid n'existe pas on renvoie une erreur,
        # sinon on peut supprimer les données

        if geonameid == None:
            resp = jsonify({'status':'fail', 'message': 'geonameid is missing'})
            resp.status_code = 400
            return resp

        else:
            element =  Content.query.filter_by(geonameid = geonameid)
            element_exists = element.first()

            if not element_exists:
                resp = jsonify({'status': 'fail', 'message' : geonameid +" does not exist in database"})
                resp.status_code = 404
                return resp
            else:
                db.session.delete(element_exists)
                db.session.commit()
                resp = jsonify({'status': 'success', 'message' : geonameid +" successfully deleted"})
                resp.status_code = 200
                return resp

class DataSearch(Resource):
    """Gere la recherche de données par filtrage en fonction des champs"""

    @token_required
    def get(self, current_user):

        params = request.args

        # on vérifie qu'au moins un filtre a été renseigné
        if not params:
            resp = jsonify({'status' : 'failed', 'message' : 'missing parameter(s) for filtering'})
            resp.status_code = 412
            return resp
        filtres = dict(params)

        # recherche
        query_object = Content.query
        try:
            # dans le cas d'un filtre alternatename, on cherche la présence d'une substring dans le champ
            if filtres.get('alternatename'):
                pattern = '%' + filtres.get('alternatename') + '%'
                query_object = query_object.filter( Content.alternatenames.like(pattern) )
                del filtres['alternatename']

            # application des autres filtres
            query_object = query_object.filter_by(**filtres)

        except sqlalchemy.exc.InvalidRequestError as e :
            resp = jsonify({'status': 'fail', 'message' : "wrong format (filter field doest not exist in db)"})
            resp.status_code = 400
            return resp

        resp = jsonify({'results' : [element.to_json() for element in query_object.all()]})
        resp.status_code = 200
        return resp
