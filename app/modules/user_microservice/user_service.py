from urllib import request

from app.shared.config.mysql_db_config import MySqlConfig


class UserService:

    def __init__(self,content):
        self.MySqlConnect = MySqlConfig()
        self.content = content

    def get_all_users(self) :
        query = "SELECT * FROM Users"
        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result
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