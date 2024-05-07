import json
from urllib import request

from app.shared.config.mysql_db_config import MySqlConfig


class UserService:

    def __init__(self,content=None):
        self.MySqlConnect = MySqlConfig()
        self.content = content

    def get_all_users_db(self):
        query = f"""
        SELECT u.*, o.name as organization_name  from Users u
            inner join Organizations o 
            where u.organization_id =o.id 

        """
        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, status
        else:
            raise Exception("Failed to fetch users from the database")


    # def get_all_users_from_organization(self, organization_id):
    #
    #     query = f"""
    #                        SELECT u.*, o.name as organization_name
    #         FROM Users u
    #         INNER JOIN Organizations o ON u.organization_id = o.id
    #         WHERE o.id = {organization_id}
    #
    #
    #            """
    #     result, status = self.MySqlConnect.execute_query(query, {})
    #     if status:
    #         return result, status
    #     else:
    #         raise Exception("Failed to fetch users from the database")

    def get_all_users_ids(self):
        query = f"""
                             SELECT ID FROM Users


                  """
        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, status
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
            last_id, status = self.MySqlConnect.get_last_inserted_id(table='Users', column='id')
            if status:
                return last_id, True
            else:
                return "Error retrieving last inserted ID", False
        else:
            raise Exception("Failed to fetch users from the database")

    def get_organization_by_user_id(self):

        query = f"""
                SELECT o.id as organization_id, o.name AS organization_name, u.name 
        FROM Organizations o INNER JOIN
        Users u 
        WHERE u.organization_id = o.id
        AND u.id = {self.content['uploader_user_id']}
        """

        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, True
        else:
            raise Exception("Failed to fetch users from the database")


    def get_all_users(self):

        query = f"""
                SELECT o.id as organization_id, o.name AS organization_name, u.name 
        FROM Organizations o INNER JOIN
        Users u 
        WHERE u.organization_id = o.id
        AND u.id = {self.content['uploader_user_id']}
        """

        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, True
        else:
            raise Exception("Failed to fetch users from the database")


    def get_all_organization_permissions(self):

        query = f"""
        SELECT p.id,p.file_id,p.permission_type,p.access_users_ids,p.uploader_user_id,o.id as organization_id
            from
            Permissions p inner join
            Organizations o 
            where 
            o.id = {self.content['organization_id']} 
        """

        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result, True
        else:
            raise Exception("Failed to fetch users from the database")

    def update_access_users_ids(self, permission_register, new_access_users_ids):
        try:
            permission_id = permission_register["id"]

            query = f"""
                   UPDATE Permissions
                   SET access_users_ids = '{new_access_users_ids}'
                   WHERE id = {permission_id}
               """
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return "Successfully updated access users ids", True
        except Exception as e:
            print(f"Error updating access_users_ids: {str(e)}")
            return False