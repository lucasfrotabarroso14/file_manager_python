
from flask import request
from flask_restful import Resource

from app.modules.file_microservice.file_service import FileService
from app.modules.user_microservice.user_model import User
from app.modules.user_microservice.user_service import UserService


class UserResource(Resource):



    def post(self):
        try:
            data = request.get_json()
            validated_user = User(**data)

            content = {
                "name": validated_user.name,
                "email": validated_user.email,
                "password": validated_user.password,
                "organization_id": validated_user.organization_id,
            }

            user_service = UserService(content)

            result, status = user_service.create_new_user_db()
            if status:
                return {
                    "status": True,
                    "status_code": 200,
                    "result": "User created",
                }
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error creating User",
                }

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }

class UserDetail(Resource):
    def get(self,user_id):
        try:
            content ={
                "user_id": user_id,
            }
            file_service = FileService(content)
            # ele vai fazer um like no campo acce_ussers_id e vai trazer todos os registros de permissao para os usuarios dentro do array de access
            user_permissions, status =file_service.get_user_permissions()
            if not status:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error fetching user permissions",
                }
            available_files = []
            #para cada registro que tenho  permissao eu vou pegar o file_id e trazer ele
            for permission in user_permissions:
                file_info, status = file_service.get_file_info(permission['file_id'])
                if status:
                    available_files.append(file_info)
            return {
                "status": True,
                "status_code": 200,
                "result": available_files,
            }


        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }





