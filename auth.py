from database import DatabaseManager
import hashlib


class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def _hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login_user(self, login, password):
        if not login or not password:
            return False, "Заполните все поля"

        hashed_password = self._hash_password(password)
        success, message = self.db.check_user_credentials(login, hashed_password)
        return success, message

    def register_user(self, login, password):
        try:
            if not login or not password:
                return False, "Заполните все обязательные поля"

            # Хешируем пароль перед сохранением
            hashed_password = self._hash_password(password)

            query = "INSERT INTO users (login, password) VALUES (%s, %s)"
            self.db.cursor.execute(query, (login, hashed_password))
            self.db.connection.commit()
            return True, "Пользователь успешно зарегистрирован"
        except Exception as e:
            return False, f"Ошибка регистрации: {e}"

    def close_connection(self):
        self.db.disconnect()