from flask import json, request, Response, redirect, render_template, url_for, session
from flask_restful import Resource
import requests

from ..config import BACKEND_URL as backend_api
from ..utils import *

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
	"""Consultation et suppression de données"""

	@login_required
	def get(self, geonameid):
		"""Affichage"""

		api_response = requests.get(backend_api + "/data/"+geonameid, headers=make_headers(), verify=False)

		if api_response.status_code == 401 :
			session.clear()
			resp = redirect(url_for('.login', error="invalid_token", next="/data/"+geonameid))
			return resp

		if api_response.status_code == 404 :
			dataAdd_rend = render_template("error.html", error_type = 404, error = 'wrong_geonameid')
			resp = Response(dataAdd_rend, status = 404, content_type="text/html")
			return resp

		result = api_response.json()['data']
		if 'modif' in dict(request.args):
			data_rend = render_template("data.html", modif=True, result = result)
		else:
			data_rend = render_template("data.html", result = result)
		resp = Response(data_rend, status=200, content_type="text/html")
		return resp

	@login_required
	def post(self, geonameid):
		"""Modifie les données"""

		info_modif = dict(request.form)
		info_modif= {k: v for k, v in info_modif.items() if v != ''}
		api_response = requests.post(backend_api + '/data/' + geonameid, headers = make_headers(), json = info_modif, verify = False)

		if api_response.status_code == 401 :
			session.clear()
			reponse = redirect(url_for('.login', error="invalid_token", next="/data/"+geonameid))
			return reponse

		resp = redirect(url_for('.data', geonameid=geonameid, modif=True))
		return resp

	@login_required
	def delete(self, geonameid):
		"""Supprime un lieu (requête delete lancée grâce à javascript)"""

		api_response = requests.delete(backend_api + "/data/"+geonameid, headers=make_headers(), verify=False)

		return api_response.status_code
