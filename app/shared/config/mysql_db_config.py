import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class MySqlConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db = os.getenv('DB_NAME')
        self._connection = None

    def get_connection(self):
        self._connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db
        )





        return self._connection

    def test_connection(self):
        try:
            connection = self.get_connection()
            if connection.is_connected():
                print("CONEXAO COM O BANCO ESTABELECIDA COM SUCESSO!!")
                return True
            else:
                print("Não foi possível estabelecer conexão com o banco de dados MySQL.")
                return False
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados MySQL:", err)
            return False

    def execute_query(self, query, params):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            formatted_query = query.strip().replace("\n", "")

            if formatted_query.split(' ')[0] == "SELECT":
                cursor.execute(formatted_query, params)
                results = cursor.fetchall()

                column_names = [desc[0] for desc in cursor.description]

                data = []
                for row in results:
                    data.append(dict(zip(column_names,row)))
                cursor.close()
                connection.close()
                return data, True

            else:
                cursor.execute(formatted_query, params)
                result = cursor.rowcount
                connection.commit()
                cursor.close()
                connection.close()

                print("Query executada com sucesso!")
                return result, True
        except mysql.connector.Error as err:
            print("Erro ao executar a query:", err)
            return str(err), False

    def get_last_inserted_id(self):
        try:
            query = f"""
            SELECT id FROM Files ORDER BY id DESC LIMIT 1
            """
            result, status = self.execute_query(query, {})

            if status:
                return result[0]['id'], True
            else :
                return "error", False
        except Exception as e:
            return str(e), False

