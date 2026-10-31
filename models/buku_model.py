from config.database import Database

class BukuModel:
    def __init__(self):
        db = Database()
        self.conn = db.get_connection()

    def get_all_buku(self):
        if not self.conn:
            return []
        try:
            cursor = self.conn.cursor()
            query = "SELECT id_buku, judul, penulis, tahun_terbit FROM buku"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error get_all_buku: {e}")
            return []

    def tambah_buku(self, judul, penulis, tahun):
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO buku (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
            cursor.execute(query, (judul, penulis, tahun))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error tambah_buku: {e}")
            return False

    def update_buku(self, id_buku, judul, penulis, tahun):
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            query = "UPDATE buku SET judul = %s, penulis = %s, tahun_terbit = %s WHERE id_buku = %s"
            cursor.execute(query, (judul, penulis, tahun, id_buku))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error update_buku: {e}")
            return False

    # Menambahkan alias ubah_buku agar sesuai dengan pemanggilan di buku_controller.py
    def ubah_buku(self, id_buku, judul, penulis, tahun):
        return self.update_buku(id_buku, judul, penulis, tahun)

    def hapus_buku(self, id_buku):
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM buku WHERE id_buku = %s"
            cursor.execute(query, (id_buku,))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error hapus_buku: {e}")
            return False