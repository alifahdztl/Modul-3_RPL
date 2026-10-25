print("=== Kalkulator Terminal Modul 3 ===")
angka1 = float(input("Masukkan angka pertama: "))
angka2 = float(input("Masukkan angka kedua: "))
hasil = angka1 + angka2

print(f"Status: Setup Berhasil!")
print(f"Hasil Penjumlahan: {hasil}")

from controllers.buku_controller import BukuController

if __name__ == "__main__":
    app = BukuController()
    app.run()