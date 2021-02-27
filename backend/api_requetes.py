# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from .utils import *

import os
import datetime
import jwt
import json


app = Flask(__name__)
api = Api(app)

app.config.from_pyfile('config.py')

from .resources import  *

api.add_resource(Login, "/", "/login")
api.add_resource(Logout, "/logout")
api.add_resource(Data, "/data", "/data/<geonameid>")
api.add_resource(DataSearch, "/data/search")
