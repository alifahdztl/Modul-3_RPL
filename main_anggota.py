# Bagian 1: Tes Kalkulator Terminal (Modul 3)
print("=== Kalkulator Terminal Modul 3 ===")
angka1 = float(input("Masukkan angka pertama: "))
angka2 = float(input("Masukkan angka kedua: "))
hasil = angka1 + angka2

print("Status: Setup Berhasil!")
print(f"Hasil Penjumlahan: {hasil}\n")

# Bagian 2: Memanggil Controller Anggota agar GUI Langsung Muncul
from controllers.anggota_controller import AnggotaController

if __name__ == "__main__":
    app = AnggotaController()
    app.run()