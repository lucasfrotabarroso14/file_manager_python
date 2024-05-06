from urllib import request

from app.shared.config.mysql_db_config import MySqlConfig


class UserService:

    def __init__(self,content=None):
        self.MySqlConnect = MySqlConfig()
        self.content = content

    def get_all_users(self) :
        query = "SELECT * FROM Users"
        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result
        else:
            raise Exception("Failed to fetch users from the database")

    def get_user_by_id(self,user_id):
        query = f"""
        SELECT * FROM Users WHERE id = {user_id}
        """
        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, True
        else:
            raise Exception("Failed to fetch users from the database")

    def create_new_user_db(self):

        query = F"""
        INSERT INTO Users (name, email, password, organization_id)
         VALUES
          ('{self.content['name']}', '{self.content['email']}', '{self.content['password']}',{self.content['organization_id']})
        """

        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, True
        else:
            raise Exception("Failed to fetch users from the database")

    def get_organization_by_user_id(self):

        query = f"""
                SELECT o.id as organization_id, o.name AS organization_name, u.name 
        FROM organizations o INNER JOIN
        users u 
        WHERE u.organization_id = o.id
        AND u.id = {self.content['uploader_user_id']}
        """

        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, True
        else:
            raise Exception("Failed to fetch users from the database")