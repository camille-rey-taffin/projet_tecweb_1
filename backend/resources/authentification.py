from flask import Flask, request, json, jsonify, make_response, Response
from flask_restful import Resource
from ..utils import *
from .users import *


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
        user = verify_user(info["name"], info["firstname"], )
        if user:
            token = make_token(user)
            resp = jsonify({'status':'success', 'User':user.to_json(), 'Token': token.decode('UTF-8')})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'status':'fail', 'message' : "Nom ou prénom incorrect"})
            resp.status_code = 400
            return resp

class Logout(Resource):
    """Logout"""

    @token_required
    def get(self, current_user):
        """Blacklist le token en cours"""

        # On récupère le token dans le header
        token = request.headers['Authorization'].split(" ")[1]
        tokens_blacklist.append(token)

        resp = jsonify({'status':'succes', 'message' : "successfully logged out"})
        resp.status_code = 400
        return resp
