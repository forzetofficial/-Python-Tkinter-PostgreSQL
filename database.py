import psycopg2
from psycopg2 import Error

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user="admin",
                password="admin",
                host="localhost",
                port="5434",
                database="mydb"
            )
            self.cursor = self.connection.cursor()
            print("Успешное подключение к PostgreSQL")
        except Error as e:
            print(f"Ошибка подключения: {e}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Отключение от PostgreSQL")

    def check_user_credentials(self, login, hashed_password):
        try:
            query = "SELECT * FROM users WHERE login = %s AND password = %s"
            self.cursor.execute(query, (login, hashed_password))
            user = self.cursor.fetchone()

            if user:
                return True, "Успешный вход!"
            else:
                return False, "Неверный логин или пароль"

        except Error as e:
            return False, f"Ошибка базы данных: {e}"