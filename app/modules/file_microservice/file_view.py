
from flask import request
from flask_restful import Resource

from app.modules.file_microservice.file_model import File
from app.modules.file_microservice.file_service import FileService
from app.modules.organization_microservice.organization_service import OrganizationService
from app.modules.user_microservice.user_model import User

import json

from app.modules.user_microservice.user_service import UserService
from app.shared.config.redis_client import RedisClient
from app.shared.helpers.celery_worker import upload_simulate_file


class FileResource(Resource):

    def get(self):
        try:
            file_service = FileService()
            all_files, status = file_service.get_all_files()
            array_with_allows_names = []
            user_service = UserService()

            for file in all_files:
                array_with_ids = json.loads(file['access_users_ids'])
                user_names = []
                for id in array_with_ids:
                    user_info, status = user_service.get_user_by_id(user_id=id)
                    if user_info:
                        user_names.append(user_info[0]['name'])
                file['access_users_names'] = user_names
                file['access_users_ids'] = array_with_ids

            print(all_files)
            return {
                "status": True,
                "status_code": 200,
                "result": all_files,
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
            content = {
                "file_name": data["file_name"],
                "file_type": data["file_type"],
                "file_size": data["file_size"],
                "uploader_user_id": data['uploader_user_id'],

                "permission_type": data.get("permission_type", "Geral"),
                "access_users_ids": [],


            }

            if content['permission_type'] == 'Publico':
                user_service = UserService(content)
                all_id_users, status = user_service.get_all_users_ids()
                array_with_allow_id = []
                for id in all_id_users:
                    array_with_allow_id.append(id['ID'])
                content["access_users_ids"] = array_with_allow_id
                file_service = FileService(content)
                new_file_id, status = file_service.upload_new_file_db()
                content["file_id"] = new_file_id
                file_service = FileService(content)
                result, status = file_service.create_access_for_users()



            elif content['permission_type'] == 'Geral':

                user_service = UserService(content)
                organization, status = user_service.get_organization_by_user_id()

                content["organization_id"] = organization[0]['organization_id']

                organization_service = OrganizationService(content)
                all_users_from_organization, status = organization_service.get_users_from_organization_by_organization_id()
                array_with_allow_users = []
                for user in all_users_from_organization:
                    array_with_allow_users.append(user['uploader_user_id'])
                content["access_users_ids"] = array_with_allow_users
                print(content["access_users_ids"])

                file_service = FileService(content)
                new_file_id, status = file_service.upload_new_file_db()
                content["file_id"] = new_file_id
                file_service = FileService(content)
                result, status = file_service.create_access_for_users()




            elif content['permission_type'] == 'Selecionados':
                file_service = FileService(content)
                new_file_id, status = file_service.upload_new_file_db()
                if status:
                    content = {
                        "file_id": new_file_id,
                        "permission_type": "Selecionados",
                        "access_users_ids": data["access_users_ids"],
                        "uploader_user_id": data["user_id"],

                    }
                    file_service = FileService(content)
                    result, status = file_service.create_access_for_users()
                    if status:
                        print('deu certo')




            if status:

                # Essa funcao abaixo vai simular um upload em segundo plano com o celery:
                # para executar o celery digite no cmd: celery -A app.shared.helpers.celery_worker worker --loglevel=info

                upload_simulate_file.delay()
                return {
                    "status": True,
                    "status_code": 200,
                    "result": "File uploaded successfully",
                }
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error uploading file",
                }

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }


class FileDetail(Resource):
    redis_client = RedisClient()



    def put(self, file_id):
        try:
            data = request.get_json()
            content = {
                "file_id": file_id,
                "permission_type": data.get("permission_type", "Geral"),
                "access_users_ids": data.get("access_users_ids", []),
            }
            #criar uma funcao que pegue todos os ids de usuarios e coloque dentro do access
            if content['permission_type'] == 'Publico':
                content['access_users_ids'] = []

            file_service = FileService(content)
            result, status = file_service.update_file_permissions()

            if status:
                return {
                    "status": True,
                    "status_code": 200,
                    "result": "File permissions updated successfully",
                }
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error updating file permissions",
                }

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }

    def delete(self, file_id):
        try:
            content = {
                "file_id": file_id,
            }
            file_service = FileService(content)
            result, status = file_service.delete_file()
            if status and result == 1:
                self.redis_client.delete_cache(f"file_{file_id}")

                return {
                    "status": True,
                    "status_code": 204,
                    "result": "File deleted successfully",
                }, 204
            elif result == 0:
                return {
                    "status": False,
                    "status_code": 404,
                    "result": "File not found",
                }, 404
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error deleting file",
                }, 500

        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),

            }






