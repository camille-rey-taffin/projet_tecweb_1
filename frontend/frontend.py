# coding: utf-8
from flask import Flask
from flask_restful import Resource, Api
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
api = Api(app)

app.config.from_pyfile('config.py')

from .resources import *

api.add_resource(Index, "/", "/index")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(DataSearch, "/data/search")
api.add_resource(DataAdd, "/data/add")
api.add_resource(Data, "/data/<geonameid>")


if __name__ == '__main__':
	app.run(debug=True)
