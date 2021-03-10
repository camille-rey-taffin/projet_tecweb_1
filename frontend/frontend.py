# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, url_for
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
api = Api(app)

# URL de notre application backend
backend_api = "https://projet-tecweb-backend.herokuapp.com"


class Login(Resource):
	"""Login"""

	def get(self):
		"""Description """
		login_rend = render_template("login.html")
		resp = Response(login_rend, status=200, content_type="text/html")

		return resp

	def post(self):
		"""Description"""
		info_login = request.form
		user_id = {"name" : info["nom"], "firstname" : info["prenom"]}
		api_response = requests.post(backend_api + '/login', json = user_id, verify = False)


		# Si les identifiants sont corrects, on enregistre le token dans un cookie
		# puis on redirige vers les données :
		if "Token" in api_response.json():
			token = api_response.json()["Token"]
			resp = redirect('/login')
			resp.headers['Authorization'] = 'Bearer ' + token
			return resp

		# Si les identifiants sont incorrects :
		elif r.json()["ERROR"] == "Username ou mot de passe incorrect":
			render_response = render_template("login_error.html", message="Identifiant ou mot de passe incorrect !")
			resp = Response(render_response, status=403, content_type="text/html")
			return resp

api.add_resource(Login, "/login")


if __name__ == '__main__':
	app.run(debug=True)
