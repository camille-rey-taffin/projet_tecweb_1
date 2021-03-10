# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, url_for, session
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "ffff"
api = Api(app)


# URL de notre application backend
backend_api = "https://projet-tecweb-backend.herokuapp.com"

class Index(Resource):
	"""Index"""

	def get(self):
		"""Description"""
		index_rend = render_template("index.html")
		resp = Response(index_rend, status=200, content_type="text/html")
		return resp

class Login(Resource):
	"""Login"""

	def get(self):
		"""Description """

		error = False

		if "error" in request.args:
			error = request.args["error"]

		if error :
			login_rend = render_template("login.html", login = False, fail = True, error = error)

		elif 'token' in session:
			login_rend = render_template("login.html", login = True, nom = session['user_name'], prenom = session['user_firstname'])

		else :
			login_rend = render_template("login.html", login = False)

		resp = Response(login_rend, status=200, content_type="text/html")

		return resp

	def post(self):
		"""Description"""
		info_login = dict(request.form)
		user_id = {"name" : info_login["name"], "firstname" : info_login["firstname"]}
		api_response = requests.post(backend_api + '/login', json = info_login, verify = False).json()


		# Si les identifiants sont corrects, on enregistre le token dans un cookie
		# puis on redirige vers les données :
		if "Token" in api_response:
			session.clear()
			session['token'] = api_response["Token"]
			session['user_id'] = api_response['User']["id"]
			session['user_name'] = api_response['User']["nom"]
			session['user_firstname'] = api_response['User']["prenom"]
			resp = redirect('/login')
			return resp

		# Si les identifiants sont incorrects :
		elif api_response["status"] == "fail":
			#render_response = render_template("login_error.html", message="Identifiant ou mot de passe incorrect !")
			login_rend = render_template("login.html", login = False, fail = True, error = "wrong_id")
			resp = Response(login_rend, status=401, content_type="text/html")
			return resp

class Logout(Resource):
	"""Login"""

	def get(self):
		"""Description """

		if 'token' in session:
			session.clear()
			reponse = redirect('/login')
			return reponse
		else :
			reponse = "erreur, vous n'étiez pas connecté"
			resp = Response(reponse, status=400, content_type="text/html")
			return resp

class DataSearch(Resource):
	"""Recherche de données"""

	def get(self):
		"""Description """
		filtres = dict(request.args)
		filtres = {k: v for k, v in filtres.items() if v != ''}
		print(filtres)
		if 'token' not in session:
			reponse = redirect(url_for('.login', error="login_required"))
			return reponse
		else :
			headers = { 'Authorization' : "Bearer " + session['token'] }

			api_response = requests.get(backend_api + "/data/search", headers=headers, params = filtres, verify=False)

			if api_response.status_code == 401 :
				session.clear()
				reponse = redirect(url_for('.login', error="invalid_token"))
				return reponse

			if not filtres :
				datasearch_rend = render_template("datasearch.html")
				resp = Response(datasearch_rend, status=200, content_type="text/html")
				return resp

			else :
				results = api_response.json()["results"]
				datasearch_rend = render_template("datasearch.html", search = True, results = results)
				resp = Response(datasearch_rend, status=200, content_type="text/html")
				return resp

api.add_resource(Index, "/", "/index")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(DataSearch, "/data/search")


if __name__ == '__main__':
	app.run(debug=True)
