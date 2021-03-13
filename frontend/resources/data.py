from flask import json, request, Response, redirect, render_template, url_for, session
from flask_restful import Resource
import requests

from ..config import BACKEND_URL as backend_api
from ..utils import *

class DataSearch(Resource):
	"""Classe de Recherche de données"""

	@login_required
	def get(self):
		"""Méthode GET, affiche la page de recherche avec le formulaire de recherche.
		Si un formulaire de recherche a été soumis, affiche les résultats dans un tableau."""

		filtres = dict(request.args)
		filtres = {k: v for k, v in filtres.items() if v != ''}

		api_response = requests.get(backend_api + "/data/search", headers = make_headers(), params = filtres, verify=False)

		# cas d'une session expirée ou invalide
		if api_response.status_code == 401 :
			#session.clear()
			#reponse = redirect(url_for('.login', error = "invalid_token", next = "/data/search"))
			#return reponse
			return invalid_token_response()

		# cas où aucune recherche n'a été effectuée
		if not filtres :
			datasearch_rend = render_template("datasearch.html")
			resp = Response(datasearch_rend, status = 200, content_type = "text/html")
			return resp

		# cas où une recherche a été effectuée
		else :
			results = api_response.json()["results"]
			datasearch_rend = render_template("datasearch.html", search = True, results = results)
			resp = Response(datasearch_rend, status = 200, content_type = "text/html")
			return resp

class DataAdd(Resource):
	"""Classe d'ajout des données"""

	@login_required
	def get(self):
		"""Méthode GET, affiche le formulaire d'ajou des données """

		dataAdd_rend = render_template("dataAdd.html")
		resp = Response(dataAdd_rend, status = 200, content_type = "text/html")
		return resp

	@login_required
	def post(self):
		"""Méthode POST, envoie une demande d'ajout des données.
		Affiche un message de succès ou un message d'erreur """

		info_ajout = dict(request.form)
		api_response = requests.put(backend_api + '/data/' + info_ajout['geonameid'], headers = make_headers(), json = info_ajout, verify = False)

		# cas d'une session expirée ou invalide
		if api_response.status_code == 401 :
			return invalid_token_response()

		# cas où le geonameid existe déjà dans la BDD
		if api_response.status_code == 409 :
			dataAdd_rend = render_template("dataAdd.html", geonameid_exists = info_ajout['geonameid'])
			resp = Response(dataAdd_rend, status = 409, content_type="text/html")
			return resp

		# succès de l'ajout
		if api_response.status_code == 200 :
			dataAdd_rend = render_template("dataAdd.html", geonameid_created = info_ajout['geonameid'])
			resp = Response(dataAdd_rend, status = 200, content_type="text/html")
			return resp

class Data(Resource):
	"""Classe de Consultation, modification et suppression de données d'un lieu"""

	@login_required
	def get(self, geonameid):
		"""Méthode GET, affiche les informations de l'élément d'id 'geonameid'
		sous forme d'un tableau"""

		api_response = requests.get(backend_api + "/data/"+geonameid, headers=make_headers(), verify=False)

		# cas d'une session expirée ou invalide
		if api_response.status_code == 401 :
			return invalid_token_response()

		# cas d'un geoname id non existant dans la BDD
		if api_response.status_code == 404 :
			dataAdd_rend = render_template("error.html", error_type = 404, error = 'wrong_geonameid')
			resp = Response(dataAdd_rend, status = 404, content_type = "text/html")
			return resp

		infos = api_response.json()['data']

		# si les informations de l'élément viennent d'être modifiées, ajout d'un message de modification
		if 'modif' in dict(request.args):
			data_rend = render_template("data.html", modif=True, infos = infos)
		else:
			data_rend = render_template("data.html", infos = infos)

		resp = Response(data_rend, status = 200, content_type = "text/html")
		return resp

	@login_required
	def post(self, geonameid):
		"""Méthode POST, modifie les informations de l'élément"""

		info_modif = dict(request.form)
		info_modif= {k: v for k, v in info_modif.items() if v != ''}
		api_response = requests.post(backend_api + '/data/' + geonameid, headers = make_headers(), json = info_modif, verify = False)

		# cas d'une session expirée ou invalide
		if api_response.status_code == 401 :
			return invalid_token_response()

		resp = redirect(url_for('.data', geonameid=geonameid, modif=True))
		return resp

	@login_required
	def delete(self, geonameid):
		"""Méthode DELETE, supprime un lieu (requête delete en AJAX + affichage d'un
		message de succès grâce à javascript, en cliquant sur bouton SUPPRIMER)"""

		api_response = requests.delete(backend_api + "/data/"+geonameid, headers = make_headers(), verify = False)

		return api_response.status_code
