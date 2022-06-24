from flask import request
from flask_restx import Namespace, Resource

from container import director_service
from dao.model.director import directors_schema, director_schema

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = director_service.get_all_directors()
        return directors_schema.dump(directors), 200

    def post(self):
        data = request.json
        directors = director_service.add_directors(data)
        return 'Object appended', 201

    def delete(self):
        pass


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        director = director_service.get_one_director(did)
        if director:
            return director_schema.dump(director), 200
        return 'Object not found', 404

    def path(self, did: int):
        req_json = request.json
        req_json['id'] = did
        director = director_service.update_partial(req_json)
        if director:
            return 'Object updated', 204
        return 'Object not found', 404

    def put(self, did: int):
        req_json = request.json
        req_json['id'] = did
        director = director_service.update_director(req_json)
        if director:
            return 'Object updated', 204
        return 'Object not found', 404

    def delete(self, did: int):
        director = director_service.delete(did)
        if director:
            return 'Object updated', 204
        return 'Object not found', 404
