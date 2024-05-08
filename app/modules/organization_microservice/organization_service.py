from app.shared.config.mysql_db_config import MySqlConfig


class OrganizationService:

    def __init__(self,content=None):
        self.MySqlConnect = MySqlConfig()
        self.content = content

    def get_all_organizations(self) :
        try:
            query = "SELECT * FROM Organizations"
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return result, True
            else:
                return "Error", False
        except Exception as e:
            return str(e), False

    def get_users_from_organization_by_organization_id(self):
        try:
            query = f"""
                        SELECT u.id as uploader_user_id, u.name 
            FROM Organizations o INNER JOIN
            Users u 
           WHERE u.organization_id = o.id
            AND o.id = {self.content['organization_id']}
            """
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return result, True
            else:
                return "Error", False
        except Exception as e:
            return str(e), False


    def create_organization_db(self):

        query = f"""
        INSERT INTO file_manager.Organizations (name) VALUES ('{self.content['organization_name']}')
        """

        try:
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return result, True
            else:
                return result, False

        except Exception as e:
            return str(e), False