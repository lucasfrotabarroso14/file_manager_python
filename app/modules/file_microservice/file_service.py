from app.shared.config.mysql_db_config import MySqlConfig
import json

class FileService:

    def __init__(self, content=None):
        self.MySqlConnect = MySqlConfig()
        self.content = content

    def get_all_files(self):
        query = f"""
        SELECT * FROM Files
        """
        result, status = self.MySqlConnect.execute_query(query, {})
        print(result)
        if status:
            return result, status
        else:
            raise Exception("Failed to fetch users from the database")

    def get_file_permissions(self):
        query = f"""
        SELECT access_users_ids FROM Permissions
        WHERE
         uploader_user_id = {self.content['uploader_user_id']}
         AND
         file_id = {self.content['file_id']}
        """
        result, status = self.MySqlConnect.execute_query(query, {})
        print(result)
        if status:
            access_array =  json.loads(result[0]['access_users_ids'])
            return access_array, status
        else:
            raise Exception("Failed to fetch users from the database")

    def upload_new_file_db(self):
        query = f"""
        INSERT INTO Files (file_name, file_type, file_size, user_id)
        VALUES ('{self.content['file_name']}', '{self.content['file_type']}',
                {self.content['file_size']}, {self.content['user_id']})
        """

        try:
            result, status = self.MySqlConnect.execute_query(query, {})

            if status:
                last_id, status = self.MySqlConnect.get_last_inserted_id()
                if status:
                    return last_id, True
                else:
                    return "Error retrieving last inserted ID", False
            else:
                return "Error inserting file data", False

        except Exception as e:
            return str(e), False
    def create_access_for_users(self):



        query = f"""
        INSERT INTO Permissions (file_id, permission_type, access_users_ids,uploader_user_id)
        VALUES ( {self.content['file_id']},
                '{self.content['permission_type']}', '{self.content['access_users_ids']}',{self.content['uploader_user_id']})
        """

        try:
            result, status = self.MySqlConnect.execute_query(query, {})
            if status:
                return result, True
            else:
                return "Error", False

        except Exception as e:
            return str(e), False

    def update_file_permissions(self):
        query = f"""
           UPDATE Permissions 
           SET permission_type = '{self.content['permission_type']}', 
               access_users_ids = '{json.dumps(self.content['access_users_ids'])}'
           WHERE file_id = {self.content['file_id']}
           """

        try:
            result, status = self.MySqlConnect.execute_query(query, {})
            return result, status

        except Exception as e:
            return str(e), False


    def delete_file(self):
        query = f"""
        DELETE FROM Files
        WHERE id = {self.content['file_id']}
        """

        try:
            result, status = self.MySqlConnect.execute_query(query, {})

            return result, status

        except Exception as e:
            return str(e), False