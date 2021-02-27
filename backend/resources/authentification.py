# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response
from flask_restful import Resource
from ..utils import *
from .users import *

class Login(Resource):
    """Ressource Login"""

    def post(self):
        """"Crée le token d'un utilisateur si les informations reçues
        correspondent bien à un compte utilisateur"""

        #On vérifie que l'utilisateur n'est pas déjà logged in
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            decoded_token = decode_token(token)
            if isinstance(decoded_token, str):
                resp = jsonify({ "status" : "success", "message" : "already logged in", "User_id" : decoded_token, "Token" : token})
                resp.status_code = 200
                return resp

        # On récupère les informations du body de la requête POST
        info = request.json

        # On vérifie que les identifiants correpondent à un utilisateur
        # Si oui on crée le token, l'utilisateur correspondant et le token sont renvoyés
        # Si non, une erreur est renvoyé
        try :
            user = verify_user(info["name"], info["firstname"])
            token = make_token(user)
            resp = jsonify({'status':'success', 'User':user.to_json(), 'Token': token.decode('UTF-8')})
            resp.status_code = 200
            return resp

        except KeyError :
            resp = jsonify({"status" : "fail", "message" : "wrong authentification fields ('name' and 'firstname' required)"})
            resp.status_code = 400
            return resp

        except ValueError :
            resp = jsonify({'status':'fail', 'message' : "Incorrect name and/or firstname"})
            resp.status_code = 401
            return resp

class Logout(Resource):
    """Ressource Logout"""

    @token_required
    def get(self, current_user):
        """Procédure de logout (blacklist le token en cours)"""

        # On récupère le token dans le header et on l'ajoute à la blacklist
        token = request.headers['Authorization'].split(" ")[1]
        tokens_blacklist.append(token)

        resp = jsonify({'status':'succes', 'message' : "successfully logged out"})
        resp.status_code = 200
        return resp
