print("=== Kalkulator Terminal Modul 3 ===")
angka1 = float(input("Masukkan angka pertama: "))
angka2 = float(input("Masukkan angka kedua: "))
hasil = angka1 + angka2

print(f"Status: Setup Berhasil!")
print(f"Hasil Penjumlahan: {hasil}")

from controllers.auth_controller import AuthController

if __name__ == "__main__":
    app = AuthController()
    app.run()
