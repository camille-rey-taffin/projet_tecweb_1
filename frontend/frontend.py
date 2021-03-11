# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, url_for, session
from flask_restful import Resource, Api
from functools import wraps
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "ffff"
api = Api(app)


# URL de notre application backend
backend_api = "https://projet-tecweb-backend.herokuapp.com"

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

		error = False if "error" not in request.args else request.args["error"]

		if error :
			login_rend = render_template("login.html", login = False, fail = True, error = error)
			resp = Response(login_rend, status=401, content_type="text/html")

		elif 'token' in session:
			login_rend = render_template("login.html", login = True, nom = session['user_name'], prenom = session['user_firstname'])
			resp = Response(login_rend, status=200, content_type="text/html")

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
			reponse = redirect('/login')
			return reponse

		else :
			reponse = "ERREUR - logout impossible (pas authentifié)"
			resp = Response(reponse, status=400, content_type="text/html")
			return resp

class DataSearch(Resource):
	"""Recherche de données"""

	@login_required
	def get(self):
		"""Description """

		filtres = dict(request.args)
		filtres = {k: v for k, v in filtres.items() if v != ''}

		api_response = requests.get(backend_api + "/data/search", headers = make_headers(), params = filtres, verify=False)

		if api_response.status_code == 401 :
			session.clear()
			reponse = redirect(url_for('.login', error="invalid_token", next="/data/search"))
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

class DataAdd(Resource):
	"""Recherche de données"""

	@login_required
	def get(self):
		"""Description """

		dataAdd_rend = render_template("dataAdd.html")
		resp = Response(dataAdd_rend, status=200, content_type="text/html")
		return resp

	@login_required
	def post(self):
		"""Description """

		info_ajout = dict(request.form)
		api_response = requests.put(backend_api + '/data/' + info_ajout['geonameid'], headers = make_headers(), json = info_ajout, verify = False)

		if api_response.status_code == 401 :
			session.clear()
			resp = redirect(url_for('.login', error="invalid_token", next="/data/add"))
			return resp

		if api_response.status_code == 409 :
			dataAdd_rend = render_template("dataAdd.html", geonameid_exists = info_ajout['geonameid'])
			resp = Response(dataAdd_rend, status = 409, content_type="text/html")
			return resp

		if api_response.status_code == 200 :

			dataAdd_rend = render_template("dataAdd.html", geonameid_created = info_ajout['geonameid'])
			resp = Response(dataAdd_rend, status = 200, content_type="text/html")
			return resp

class Data(Resource):
	"""Consultation, modification et suppression de données"""

	@login_required
	def get(self, geonameid):
		"""Affichage"""

		api_response = requests.get(backend_api + "/data/" + geonameid, headers = make_headers(), verify = False)

		if api_response.status_code == 401 :
			session.clear()
			reponse = redirect(url_for('.login', error="invalid_token", next="/data/" + geonameid))
			return reponse

		result = api_response.json()['data']
		data_rend = render_template("data.html", search = True, result = result)
		resp = Response(data_rend, status=200, content_type="text/html")
		return resp


api.add_resource(Index, "/", "/index")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(DataSearch, "/data/search")
api.add_resource(DataAdd, "/data/add")
api.add_resource(Data, "/data/<geonameid>")


if __name__ == '__main__':
	app.run(debug=True)
