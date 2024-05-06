
from flask import request
from flask_restful import Resource

from app.modules.file_microservice.file_model import File
from app.modules.file_microservice.file_service import FileService
from app.modules.user_microservice.user_model import User



class FileResource(Resource):

    def get(self):
        try:

            file_service = FileService()
            result, status = file_service.get_all_files()

            if status:
                return {
                    "status": True,
                    "status_code": 200,
                    "result": result,
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



    def post(self):
        try:
            data = request.get_json()
            content = {
                "file_name": data["file_name"],
                "file_type": data["file_type"],
                "file_size": data["file_size"],
                "user_id": data['user_id'],

                "permission_type": data.get("permission_type", "Geral"),
                "access_users_ids": [],


            }
            if content['permission_type'] == 'Geral':
                file_service = FileService(content)
                new_file_id, status = file_service.upload_new_file_db()

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



    def put(self, file_id):
        try:
            data = request.get_json()
            content = {
                "file_id": file_id,
                "permission_type": data.get("permission_type", "Geral"),
                "access_users_ids": data.get("access_users_ids", []),
            }
            if content['permission_type'] == 'Geral':
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






