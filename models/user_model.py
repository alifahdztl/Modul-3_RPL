import hashlib
import pymysql
from config.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def autentikasi(self, username, password):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                password_hash = self.hash_password(password)

                query = f"SELECT id_user, username, role FROM {self.table_name} WHERE BINARY username = %s AND password = %s"
                cursor.execute(query, (username, password_hash))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                return user
            except Exception as e:
                print("Error autentikasi:", e)
                if conn:
                    conn.close()
        return None