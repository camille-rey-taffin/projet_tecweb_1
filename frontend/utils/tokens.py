from flask import request, redirect, url_for, session
from functools import wraps

def login_required(f):
	"""Décorateur pour les pages avec login requis. Permet de rrediriger vers la page de login puis vers la page sur laquelle on était."""
	@wraps(f)
	def decorator(*args, **kwargs):
		if 'token' not in session:
			reponse = redirect(url_for('.login', error="login_required", next = request.path))
			return reponse
		else :
			return f(*args, **kwargs)
	return decorator

def make_headers():
	return { 'Authorization' : "Bearer " + session['token'] }
