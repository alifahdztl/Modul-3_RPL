import mysql.connector
from models.anggota_model import AnggotaModel

# 1. Konfigurasi Koneksi Database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="perpustakaan"  # Sesuaikan dengan nama database Anda
)
model_anggota = AnggotaModel(db_connection)

print("\nMenambahkan data Anggota baru...")
model_anggota.insert_anggota("Budi Santoso", "Jl. Merdeka No. 00")
model_anggota.insert_anggota("Siti Aisyah", "Jl. Pangeran No. 12")
print("Data anggota berhasil ditambahkan!")

print("\n=== Daftar Anggota Perpustakaan ===")
daftar_anggota = model_anggota.get_all_anggota()
if daftar_anggota:
    for anggota in daftar_anggota:
        print(f"[{anggota['id_anggota']}] Nama: {anggota['nama']} | Alamat: {anggota['alamat']}")
else:
    print("Tabel anggota kosong")

# Tutup koneksi database
db_connection.close()