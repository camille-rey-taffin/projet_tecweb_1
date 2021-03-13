from flask import json, request, Response, redirect, render_template, url_for, session
from flask_restful import Resource
import requests

from ..config import BACKEND_URL as backend_api
from ..utils import *

class Login(Resource):
	"""Classe du Login"""

	def get(self):
		""" Méthode GET, affiche le formulaire de login si l'utilisateur n'est pas connecté.
		Un message peut accompagner ce formulaire en fonction du contexte.
		Affiche un message d'accueil et un bouton de déconnexion si l'utilisateur est déjà connecté. """

		error = False if "error" not in request.args else request.args["error"]

		# cas où l'utilisateur a été redirigé vers la page de login depuis une autre page
		if error :
			login_rend = render_template("login.html", login = False, fail = True, error = error)
			resp = Response(login_rend, status = 401, content_type = "text/html")

		# cas où l'utilisateur est déjà connecté
		elif 'token' in session:
			login_rend = render_template("login.html", login = True, nom = session['user_name'], prenom = session['user_firstname'])
			resp = Response(login_rend, status=200, content_type="text/html")


		else :
			# cas où l'utilisateur vient de se déconnecter
			if "logout" in request.args :
				login_rend = render_template("login.html", login = False, logout = True)

			# cas standard
			else :
				login_rend = render_template("login.html", login = False)

			resp = Response(login_rend, status=200, content_type="text/html")

		return resp

	def post(self):
		"""Méthode POST, envoie une demande de login à l'api backend à partir des
		informations du formulaire de login."""

		info_login = dict(request.form)
		api_response = requests.post(backend_api + '/login', json = info_login, verify = False)

		next_page = False if "next" not in request.args else request.args["next"]

		# Si les identifiants sont correct, on enregistre le token dans la session
		if api_response.status_code == 200:
			session.clear()
			api_response = api_response.json()
			session['token'] = api_response["Token"]
			session['user_id'] = api_response['User']["id"]
			session['user_name'] = api_response['User']["nom"]
			session['user_firstname'] = api_response['User']["prenom"]
			if next_page:
				# redirection vers la page que l'utilisateur essayait de consulter avant login
				resp = redirect(next_page)
			else :
				resp = redirect('/login')
			return resp

		# Si les identifiants sont incorrects, on affiche à nouveau le formulaire, avec un message d'erreur
		elif api_response.status_code == 401:
			login_rend = render_template("login.html", login = False, fail = True, error = "wrong_id")
			resp = Response(login_rend, status = 401, content_type = "text/html")
			return resp

class Logout(Resource):
	"""Classe Logout"""

	def get(self):
		"""Méthode GET, permet la déconnexion de l'utilisateur."""

		reponse_api = requests.get(backend_api + '/logout', headers = make_headers(), verify = False)
		if reponse_api.status_code == 200 :
			session.clear()
			reponse = redirect(url_for('.login', logout = True))
			return reponse

		# si on essaie d'accéder à /logout sans être connecté, ou avec un token expiré/invalide
		else :
			session.clear()
			logout_rend = render_template("error.html", error_type = 400)
			resp = Response(logout_rend, status = 400, content_type = "text/html")
			return resp
