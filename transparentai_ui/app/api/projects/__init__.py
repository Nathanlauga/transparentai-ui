from flask import Response, request
from flask_restplus import Resource
import json

from ...models import Project, JSONEncoder

class ProjectsApi(Resource):
    def get(self):
        projects = [p.to_dict() for p in Project.query.all()]
        return Response(json.dumps(projects, cls=JSONEncoder), mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        movie = Project(**body).save()
        id = movie.id
        return {'id': str(id)}, 200


class ProjectApi(Resource):
    def put(self, id):
        body = request.get_json()
        Project.get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        movie = Project.get(id=id).delete()
        return '', 200

    def get(self, id):
        movies = Project.get(id=id).to_dict()
        return Response(movies, mimetype="application/json", status=200)


def initialize_projects_routes(api):
    api.add_resource(ProjectsApi, '/api/projects')
    api.add_resource(ProjectApi, '/api/projects/<id>')
