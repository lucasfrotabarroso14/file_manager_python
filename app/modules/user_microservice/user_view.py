
from flask import request
from flask_restful import Resource

from app.modules.file_microservice.file_service import FileService
from app.modules.user_microservice.user_model import User
from app.modules.user_microservice.user_service import UserService
from app.shared.config.redis_client import RedisClient

import json
class UserResource(Resource):

    def get(self):
        try:
            user_service = UserService()
            all_users, status = user_service.get_all_users_db()
            if status:
                return {
                    "status": True,
                    "status_code": 200,
                    "result": all_users,
                }
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error",
                }
        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }





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

            new_user_id, status = user_service.create_new_user_db()
            content['user_id'] = new_user_id

            # depois que eu criar o usuario tenho que adicionar ele em todos os arrays de access para a organizacao dele
            # tenho que retornar todos os ids dos registros de permissao  que preciso fazer o update
            #funcao para atualizar todos os access das permissions adicionando o id do usuario nos arrays de access_users_ids
            if status:
                organization_permissions, status = user_service.get_all_organization_permissions()
                if status and len(organization_permissions) > 0:
                    for permission_register in organization_permissions:
                        access_users_ids = json.loads(permission_register['access_users_ids'])

                        access_users_ids.append(content['user_id'])
                        result, status = user_service.update_access_users_ids(permission_register, access_users_ids)
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
                return {
                        "status": True,
                        "status_code": 200,
                        "result": "User created",
                    }

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }

class UserDetail(Resource):
    def __init__(self):
        self.redis_client = RedisClient()

    def get(self, user_id):
        try:
            content = {
                "user_id": user_id,
            }
            file_service = FileService(content)

            user_permissions, status = file_service.get_user_permissions()
            if not status:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error fetching user permissions",
                }

            available_files = []
            for permission in user_permissions:
                file_info, status = file_service.get_file_info(permission['file_id'])
                if status:
                    available_files.append(file_info)

            response = {
                "status": True,
                "status_code": 200,
                "result": available_files,
            }


            if available_files:

                file_id = available_files[0]['id']

                cached_data = self.redis_client.get_cache(f"file_{file_id}")
                if cached_data is not None and len(cached_data.get('result', [])) > 0:
                    return cached_data
                else:

                    self.redis_client.set_cache(f"file_{file_id}", response)

            return response

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }








