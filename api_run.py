from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class HelloErtim(Resource):
    def get(self):
        return {'hello': 'world'}

class Etudiants(Resource):
    def get(self):
        return {'type': 'etudiants'}
    def post(self):
        return {'hello': "je viens de créer un étudiant"}
    def delete(self):
        return {'hello': 'world'}

class CreateUserErtim(Resource):
    def post(self, id_user):
        data = request.json
        return {'user_post': data, 'name': 'dddd'}

api.add_resource(HelloErtim, '/')
api.add_resource(Etudiants, '/etudiants')
api.add_resource(CreateUserErtim, '/user/<id_user>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=True, debug=True)
