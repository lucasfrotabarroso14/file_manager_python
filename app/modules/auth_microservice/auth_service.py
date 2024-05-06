from app.shared.config.mysql_db_config import MySqlConfig


class AuthService:

    def __init__(self):
        self.MySqlConnect = MySqlConfig()

    def get_all_users(self) :
        query = "SELECT * FROM Users"
        result, status = self.MySqlConnect.execute_query(query, {})
        if status:
            return result
        else:
            raise Exception("Failed to fetch users from the database")