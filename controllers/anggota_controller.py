import tkinter.messagebox as messagebox
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

        # Binding tombol-tombol di View
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        if hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.perbarui_data)
        elif hasattr(self.view, 'btn_perbarui'):
            self.view.btn_perbarui.configure(command=self.perbarui_data)
            
        if hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)

        # Event klik tabel untuk mengisi form
        self.view.tabel.bind("<ButtonRelease-1>", self.isi_form_dari_tabel)

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

    def isi_form_dari_tabel(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_values = self.view.tabel.item(selected_item, 'values')
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_nama.insert(0, item_values[1])
            self.view.entry_alamat.delete(0, 'end')
            self.view.entry_alamat.insert(0, item_values[2])

    def perbarui_data(self):
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data anggota yang ingin diperbarui!")
            return

        item_values = self.view.tabel.item(selected_item, 'values')
        id_anggota = item_values[0]

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(id_anggota, nama, alamat)

        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.view.entry_nama.delete(0, 'end')
            self.view.entry_alamat.delete(0, 'end')
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
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def run(self):
        self.view.mainloop()