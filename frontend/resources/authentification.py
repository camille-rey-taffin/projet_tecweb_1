from flask import json, request, Response, redirect, render_template, url_for, session
from flask_restful import Resource
import requests

from ..config import BACKEND_URL as backend_api
from ..utils import *

class Login(Resource):
	"""Login"""

	def get(self):
		"""Description """

		error = False if "error" not in request.args else request.args["error"]

		if error :
			login_rend = render_template("login.html", login = False, fail = True, error = error)
			resp = Response(login_rend, status=401, content_type="text/html")

		elif 'token' in session:
			login_rend = render_template("login.html", login = True, nom = session['user_name'], prenom = session['user_firstname'])
			resp = Response(login_rend, status=200, content_type="text/html")

		else :
			if "logout" in request.args :
				login_rend = render_template("login.html", login = False, logout = True)
			else :
				login_rend = render_template("login.html", login = False)
			resp = Response(login_rend, status=200, content_type="text/html")

		return resp

	def post(self):
		"""Description"""
		info_login = dict(request.form)
		api_response = requests.post(backend_api + '/login', json = info_login, verify = False)

		next_page = False if "next" not in request.args else request.args["next"]
		# Si les identifiants sont corrects, on enregistre le token dans un cookie
		# puis on redirige vers les données :
		if api_response.status_code == 200:
			session.clear()
			api_response = api_response.json()
			session['token'] = api_response["Token"]
			session['user_id'] = api_response['User']["id"]
			session['user_name'] = api_response['User']["nom"]
			session['user_firstname'] = api_response['User']["prenom"]
			if next_page:
				resp = redirect(next_page)
			else :
				resp = redirect('/login')
			return resp

		# Si les identifiants sont incorrects :
		elif api_response.status_code == 401:
			login_rend = render_template("login.html", login = False, fail = True, error = "wrong_id")
			resp = Response(login_rend, status=401, content_type="text/html")
			return resp

class Logout(Resource):
	"""Login"""

	def get(self):
		"""Description """

		if 'token' in session:
			session.clear()
			#api_response = requests.get(backend_api + '/logout', headers = make_headers(), verify = False)
			reponse = redirect(url_for('.login', logout = True))
			return reponse

		else :
			logout_rend = render_template("error.html", error_type = 400)
			resp = Response(logout_rend, status=400, content_type="text/html")
			return resp
