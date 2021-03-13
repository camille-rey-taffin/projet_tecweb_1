from flask import request, redirect, url_for, session
from functools import wraps

def login_required(f):
	"""Décorateur pour les pages avec login requis. Permet de rediriger vers
	la page de login, puis vers la page sur laquelle on était une fois l'authentification faite."""

	@wraps(f)
	def decorator(*args, **kwargs):
		if 'token' not in session:
			reponse = redirect(url_for('.login', error = "login_required", next = request.path))
			return reponse
		else :
			return f(*args, **kwargs)
	return decorator

def make_headers():
	"""Fonction pour créer les headers à envoyer dans une requête (le token)"""
	try :
		return { 'Authorization' : "Bearer " + session['token'] }
	except :
		return {}

def invalid_token_response():
	"""Fonction pour créer une réponse de redirection vers la page de login
	en cas de token invalide"""
	session.clear()
	reponse = redirect(url_for('.login', error = "invalid_token", next = request.path))
	return reponse
