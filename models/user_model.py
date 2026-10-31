import hashlib
import pymysql
from config.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()

    @staticmethod
    def hash_password(password):
        # Menggunakan SHA-256 untuk hashing password secara konsisten
        return hashlib.sha256(password.encode()).hexdigest()

    def autentikasi(self, username, password):
        if not self.conn:
            self.conn = self.db.get_connection()
        
        if self.conn:
            try:
                # Menggunakan DictCursor agar hasil fetch berupa dictionary
                cursor = self.conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT * FROM user WHERE username = %s AND password = %s"
                cursor.execute(query, (username, self.hash_password(password)))
                result = cursor.fetchone()
                cursor.close()
                return result
            except Exception as e:
                print("Error autentikasi:", e)
        return None