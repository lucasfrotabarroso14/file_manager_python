from flask import Blueprint
from flask_restful import Api

from app.modules.file_microservice.file_view import FileResource, FileDetail
from app.modules.organization_microservice.organization_view import OrganizationResource
from app.modules.user_microservice.user_view import UserResource

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)



api.add_resource(OrganizationResource,'/organizations')
api.add_resource(UserResource,'/users')
api.add_resource(FileResource,'/file')
api.add_resource(FileDetail, "/file/<int:file_id>")
