class AnggotaModel:
    def __init__(self, connection):
        self.conn = connection
        self.table_name = "anggota"

    def get_all_anggota(self):
        """Metode Read: Mengambil semua data anggota"""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def insert_anggota(self, nama, alamat):
        """Metode Create: Menambahkan data anggota baru"""
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama, alamat) VALUES (%s, %s)"
            val = (nama, alamat)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False