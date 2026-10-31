from models.anggota_model import AnggotaModel

# Inisialisasi model anggota
model_anggota = AnggotaModel()

print("\nMenambahkan data Anggota baru...")
model_anggota.tambah_anggota("Budi Santoso", "Jl. Merdeka No. 00")
model_anggota.tambah_anggota("Siti Aisyah", "Jl. Pangeran No. 12")
print("Data anggota berhasil ditambahkan!")

print("\n=== Daftar Anggota Perpustakaan ===")
daftar_anggota = model_anggota.get_all_anggota()
if daftar_anggota:
    for anggota in daftar_anggota:
        print(f"[{anggota['id_anggota']}] Nama: {anggota['nama']} | Alamat: {anggota['alamat']}")
else:
    print("Tabel anggota kosong")