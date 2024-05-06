from app.shared.config.mysql_db_config import MySqlConfig


class OrganizationService:

    def __init__(self,content):
        self.MySqlConnect = MySqlConfig()
        self.content = content

    def get_all_organizations(self) :
        try:
            query = "SELECT * FROM Organization"
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return result, True
            else:
                return "Error", False
        except Exception as e:
            return str(e), False


    def create_organization_db(self):

        query = f"""
        INSERT INTO Organizations (name) VALUES ('{self.content['organization_name']}')
        """

        try:
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return result, True
            else:
                return "Error", False

        except Exception as e:
            return str(e), False