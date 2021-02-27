from flask import Flask, request, json, jsonify
from functools import wraps
import datetime
import jwt
from ..config import SECRET_KEY

tokens_blacklist = []

def make_token(user):
    """Crée le token d'authentification"""
    encode_params = {
        "id": user.id,
        "exp": datetime.datetime.utcnow()+\
        datetime.timedelta(minutes=30)
        }
    try:
        token = jwt.encode(encode_params, SECRET_KEY, algorithm='HS256')
        return token
    except jwt.ExpiredSignatureError:
        return "token expired!"


def decode_token(token):

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
        if not isinstance(decoded_token, str):
            return decoded_token

        else :
            current_user = decoded_token
            return f(current_user, *args, **kwargs)
    return decorator
