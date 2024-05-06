
from flask import request
from flask_restful import Resource
from app.modules.organization_microservice.organization_model import Organization
from app.modules.organization_microservice.organization_service import OrganizationService


class OrganizationResource(Resource):

    def get(self):
        try:
            organization_service = OrganizationService()
            organizations, status = organization_service.get_all_organizations()
            if status:
                return {
                    "status": True,
                    "status_code": 200,
                    "result": organizations,
                }
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": 'failed to get organizations',

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
            validated_organization = Organization(**data)

            content = {
                "organization_name": validated_organization.organization_name,
            }


            organization_service = OrganizationService(content)

            result, status = organization_service.create_organization_db()
            if status:
                return {
                    "status": True,
                    "status_code": 200,
                    "result": "Organization created",
                }
            else:
                return {
                    "status": False,
                    "status_code": 500,
                    "result": "Error creating organization",
                }


        except Exception as e:
            return {
                "status": False,
                "status_code": 500,
                "result": str(e),
            }




