import pymysql
from config.database import Database

class AnggotaModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "anggota"

    def get_all_anggota(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {self.table_name}")
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            except Exception as e:
                print("Error get_all_anggota:", e)
                if conn:
                    conn.close()
        return []

    def tambah_anggota(self, nama, alamat, telepon):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"INSERT INTO {self.table_name} (nama, alamat, telepon) VALUES (%s, %s, %s)"
                cursor.execute(query, (nama, alamat, telepon))
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except Exception as e:
                print("Error tambah_anggota:", e)
                if conn:
                    conn.rollback()
                    conn.close()
        return False

    def ubah_anggota(self, id_anggota, nama, alamat, telepon):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"UPDATE {self.table_name} SET nama=%s, alamat=%s, telepon=%s WHERE id_anggota=%s"
                cursor.execute(query, (nama, alamat, telepon, id_anggota))
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except Exception as e:
                print("Error ubah_anggota:", e)
                if conn:
                    conn.rollback()
                    conn.close()
        return False

    def hapus_anggota(self, id_anggota):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"DELETE FROM {self.table_name} WHERE id_anggota=%s"
                cursor.execute(query, (id_anggota,))
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except Exception as e:
                print("Error hapus_anggota:", e)
                if conn:
                    conn.rollback()
                    conn.close()
        return False