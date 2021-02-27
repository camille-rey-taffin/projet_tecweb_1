# coding: utf-8

from flask import Flask, request, json, jsonify
from functools import wraps
import datetime
import jwt
from ..config import SECRET_KEY

tokens_blacklist = []

def make_token(user):
    """Crée un token d'authentification valable 60 mins """

    encode_params = {
        "id": user.id,
        "exp": datetime.datetime.utcnow()+\
        datetime.timedelta(minutes = 60)
        }

    token = jwt.encode(encode_params, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    """ Décode un token en paramètre """

    # vérification que le token n'est pas blacklisté (typiquement les tokens après logout)
    if token in tokens_blacklist:
            resp = jsonify({'status':'fail', 'message': 'expired token'})
            resp.status_code = 401
            return resp
    else :
        try:
            data = jwt.decode(token, SECRET_KEY)
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
    """ Décorateur qui permet de restreindre l'accès à des ressources, en vérifiant
    la présence d'un token d'identification correct dans le Authorization du header"""

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # On vérifie s'il existe un token d'authentification dans le header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            resp = jsonify({'status':'fail', 'message': 'missing token'})
            resp.status_code = 403
            return resp

        #on décode le token
        decoded_token = decode_token(token)

        # si la fonction renvoie un message d'erreur, on renvoie ce message d'erreur
        if not isinstance(decoded_token, str):
            return decoded_token

        else :
            current_user = decoded_token
            return f(current_user, *args, **kwargs)

    return decorator
