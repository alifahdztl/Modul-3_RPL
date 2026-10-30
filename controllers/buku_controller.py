import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.selected_id = None  # Menyimpan ID buku yang sedang dipilih pada tabel

        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol-tombol aksi
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_delete.configure(command=self.delete_data)
        self.view.btn_logout.configure(command=self.logout)

        # Binding event klik pada tabel untuk mengisi form otomatis
        self.view.tabel.bind("<<TreeviewSelect>>", self.item_terpilih)

        # Otorisasi Role Anggota
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled")
            self.view.btn_delete.configure(state="disabled")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    def item_terpilih(self, event):
        """Mengambil data dari baris tabel yang diklik dan memasukkannya ke form input"""
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_data = self.view.tabel.item(selected_item)['values']
            self.selected_id = item_data[0]  # ID Buku

            # Masukkan data ke entry form
            self.view.entry_judul.delete(0, "end")
            self.view.entry_judul.insert(0, item_data[1])

            self.view.entry_penulis.delete(0, "end")
            self.view.entry_penulis.insert(0, item_data[2])

            self.view.entry_tahun.delete(0, "end")
            self.view.entry_tahun.insert(0, item_data[3])

    def simpan_data(self):
        if self.user_role != "admin":
            return
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.muat_data_tabel()
            self.bersihkan_form()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def update_data(self):
        if self.user_role != "admin":
            return
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin diperbarui dari tabel!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if self.model.update_buku(self.selected_id, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.muat_data_tabel()
            self.bersihkan_form()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data.")

    def delete_data(self):
        if self.user_role != "admin":
            return
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data buku yang ingin dihapus dari tabel!")
            return

        if messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus data buku ini?"):
            if self.model.delete_buku(self.selected_id):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.muat_data_tabel()
                self.bersihkan_form()
            else:
                messagebox.showerror("Error", "Gagal menghapus data.")

    def bersihkan_form(self):
        self.selected_id = None
        self.view.entry_judul.delete(0, "end")
        self.view.entry_penulis.delete(0, "end")
        self.view.entry_tahun.delete(0, "end")

    def logout(self):
        if messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin keluar?"):
            self.view.destroy()
            from controllers.auth_controller import AuthController
            auth_app = AuthController()
            auth_app.run()

    def run(self):
        self.view.mainloop()