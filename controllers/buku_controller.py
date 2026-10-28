import tkinter.messagebox as messagebox
from tkinter import simpledialog
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self):
        # Inisialisasi Model tanpa argumen
        self.model = BukuModel()
        self.view = BukuView()

        # Menyimpan ID yang sedang dipilih untuk proses update/delete
        self.id_terpilih = None

        # Binding tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        
        if hasattr(self.view, 'btn_perbarui'):
            self.view.btn_perbarui.configure(command=self.perbarui_data)
        elif hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.perbarui_data)

        # Binding event klik tabel untuk mengambil ID buku yang dipilih
        self.view.tabel.bind("<ButtonRelease-1>", self.pilih_data)

        # Memuat data ke tabel saat aplikasi pertama kali dibuka
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            # Menggunakan 'id_buku' agar sesuai dengan database MySQL kamu
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def pilih_data(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_values = self.view.tabel.item(selected_item, 'values')
            # Simpan ID buku yang dipilih
            self.id_terpilih = item_values[0]

    def simpan_data(self):
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def hapus_data(self):
        selected_item = self.view.tabel.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus!")
            return

        item_values = self.view.tabel.item(selected_item, 'values')
        id_buku = item_values[0]

        konfirmasi = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus buku dengan ID {id_buku}?")
        if konfirmasi:
            berhasil = self.model.delete_buku(id_buku)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_tahun.delete(0, 'end')
                self.id_terpilih = None
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def perbarui_data(self):
        if not self.id_terpilih:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin diperbarui terlebih dahulu!")
            return

        selected_item = self.view.tabel.selection()
        item_values = self.view.tabel.item(selected_item, 'values')
        judul_lama = item_values[1]
        penulis_lama = item_values[2]
        tahun_lama = item_values[3]

        # 1. Pop-up untuk mengubah Judul Buku
        judul_baru = simpledialog.askstring("Ubah Judul Buku", "Masukkan judul baru:", initialvalue=judul_lama)
        if judul_baru is None:
            return

        # 2. Pop-up untuk mengubah Penulis
        penulis_baru = simpledialog.askstring("Ubah Penulis Buku", "Masukkan penulis baru:", initialvalue=penulis_lama)
        if penulis_baru is None:
            return

        # 3. Pop-up untuk mengubah Tahun Terbit
        tahun_baru = simpledialog.askstring("Ubah Tahun Terbit", "Masukkan tahun terbit baru:", initialvalue=str(tahun_lama))
        if tahun_baru is None:
            return

        if not judul_baru.strip() or not penulis_baru.strip() or not tahun_baru.strip():
            messagebox.showwarning("Peringatan", "Semua kolom input baru tidak boleh kosong!")
            return

        berhasil = self.model.update_buku(self.id_terpilih, judul_baru, penulis_baru, tahun_baru)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
            self.id_terpilih = None
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    def run(self):
        self.view.mainloop()