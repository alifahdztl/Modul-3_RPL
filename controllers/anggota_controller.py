import tkinter.messagebox as messagebox
from tkinter import simpledialog
import mysql.connector
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        # 1. Membuat koneksi database ke database 'perpustakaan'
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="perpustakaan"
        )

        # 2. Inisialisasi Model dengan mengirimkan koneksi database
        self.model = AnggotaModel(self.db_connection)
        self.view = AnggotaView()

        # Menyimpan ID yang sedang dipilih untuk proses update/delete
        self.id_terpilih = None

        # Binding tombol-tombol di View
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        if hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.perbarui_data)
        elif hasattr(self.view, 'btn_perbarui'):
            self.view.btn_perbarui.configure(command=self.perbarui_data)
            
        if hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)

        # Event klik tabel untuk mengambil ID data yang dipilih
        self.view.tabel.bind("<ButtonRelease-1>", self.pilih_data)

        # Memuat data ke tabel saat pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_anggota = self.model.get_all_anggota()
        for anggota in data_anggota:
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.insert_anggota(nama, alamat)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def pilih_data(self, event):
        # Mengambil baris yang sedang dipilih di tabel (Treeview)
        selected_item = self.view.tabel.selection()
        if selected_item:
            item = self.view.tabel.item(selected_item)
            values = item['values']
            
            # Simpan ID yang dipilih saja
            self.id_terpilih = values[0]

    def perbarui_data(self):
        if not self.id_terpilih:
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel yang ingin diperbarui terlebih dahulu!")
            return

        # Ambil data lama berdasarkan baris yang diklik di tabel
        selected_item = self.view.tabel.selection()
        item_values = self.view.tabel.item(selected_item, 'values')
        nama_lama = item_values[1]
        alamat_lama = item_values[2]

        # 1. Munculkan pop-up input untuk mengubah Nama
        nama_baru = simpledialog.askstring("Ubah Nama Anggota", "Masukkan nama baru:", initialvalue=nama_lama)
        if nama_baru is None:  # Jika pengguna menekan tombol Cancel
            return

        # 2. Munculkan pop-up input untuk mengubah Alamat
        alamat_baru = simpledialog.askstring("Ubah Alamat Anggota", "Masukkan alamat baru:", initialvalue=alamat_lama)
        if alamat_baru is None:  # Jika pengguna menekan tombol Cancel
            return

        if not nama_baru.strip() or not alamat_baru.strip():
            messagebox.showwarning("Peringatan", "Nama dan alamat baru tidak boleh kosong!")
            return

        # Proses update ke database
        berhasil = self.model.update_anggota(self.id_terpilih, nama_baru, alamat_baru)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
            self.id_terpilih = None
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def hapus_data(self):
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang ingin dihapus!")
            return

        item_values = self.view.tabel.item(selected_item, 'values')
        id_anggota = item_values[0]

        konfirmasi = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus anggota dengan ID {id_anggota}?")
        if konfirmasi:
            berhasil = self.model.delete_anggota(id_anggota)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.view.entry_nama.delete(0, 'end')
                self.view.entry_alamat.delete(0, 'end')
                self.id_terpilih = None
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def run(self):
        self.view.mainloop()