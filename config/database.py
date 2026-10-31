import pymysql

class Database:
    def __init__(self):
        self.host = "localhost"
        self.db_name = "perpustakaan"
        self.username = "root"
        self.password = ""
        self.conn = None

    def get_connection(self):
        try:
            # Hubungkan tanpa cursorclass agar aman dari error versi pymysql
            self.conn = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name
            )
            return self.conn
        except Exception as e:
            print(f"Koneksi Gagal: {e}")
            return None