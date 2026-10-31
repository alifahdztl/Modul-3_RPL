import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, parent=None, main_app=None, user_role=None):
        self.parent = parent
        self.main_app = main_app
        self.user_role = user_role
        
        self.model = BukuModel()
        self.view = BukuView(self)
        self.selected_id = None
        self.load_data()
        self.run()

    def load_data(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
            
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            if isinstance(buku, dict):
                id_buku = buku.get('id_buku', buku.get('id', ''))
                judul = buku.get('judul', '')
                penulis = buku.get('penulis', '')
                tahun = buku.get('tahun', buku.get('tahun_terbit', ''))
                if not tahun and len(buku) >= 4:
                    vals = list(buku.values())
                    tahun = vals[3] if len(vals) > 3 else ''

                self.view.tree.insert("", "end", values=(id_buku, judul, penulis, tahun))
            elif isinstance(buku, (list, tuple)):
                id_buku = buku[0] if len(buku) > 0 else ''
                judul = buku[1] if len(buku) > 1 else ''
                penulis = buku[2] if len(buku) > 2 else ''
                tahun = buku[3] if len(buku) > 3 else ''
                self.view.tree.insert("", "end", values=(id_buku, judul, penulis, tahun))

    def pilih_buku_action(self, event):
        selected_item = self.view.tree.selection()
        if selected_item:
            item_data = self.view.tree.item(selected_item)
            values = item_data['values']
            if values:
                self.selected_id = values[0]
                if hasattr(self.view, 'entry_judul'):
                    self.view.entry_judul.delete(0, 'end')
                    self.view.entry_judul.insert(0, values[1])
                
                if hasattr(self.view, 'entry_penulis'):
                    self.view.entry_penulis.delete(0, 'end')
                    self.view.entry_penulis.insert(0, values[2])
                
                if hasattr(self.view, 'entry_tahun'):
                    self.view.entry_tahun.delete(0, 'end')
                    self.view.entry_tahun.insert(0, values[3])

    def tambah_buku_action(self):
        judul = self.view.entry_judul.get() if hasattr(self.view, 'entry_judul') else ""
        penulis = self.view.entry_penulis.get() if hasattr(self.view, 'entry_penulis') else ""
        tahun = self.view.entry_tahun.get() if hasattr(self.view, 'entry_tahun') else ""

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom (Judul, Penulis, Tahun) wajib diisi!")
            return

        if self.model.tambah_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror("Gagal", "Terjadi kesalahan saat menyimpan data ke database.")

    def update_buku_action(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih dulu data buku dari tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get() if hasattr(self.view, 'entry_judul') else ""
        penulis = self.view.entry_penulis.get() if hasattr(self.view, 'entry_penulis') else ""
        tahun = self.view.entry_tahun.get() if hasattr(self.view, 'entry_tahun') else ""

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi untuk memperbarui data!")
            return

        if self.model.ubah_buku(self.selected_id, judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror("Gagal", "Terjadi kesalahan saat memperbarui data.")

    def hapus_buku_action(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih dulu data buku dari tabel yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data buku ini?"):
            if self.model.hapus_buku(self.selected_id):
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror("Gagal", "Terjadi kesalahan saat menghapus data.")

    def clear_form(self):
        self.selected_id = None
        if hasattr(self.view, 'entry_judul'):
            self.view.entry_judul.delete(0, 'end')
        if hasattr(self.view, 'entry_penulis'):
            self.view.entry_penulis.delete(0, 'end')
        if hasattr(self.view, 'entry_tahun'):
            self.view.entry_tahun.delete(0, 'end')

    def logout(self):
        self.view.destroy()
        if self.main_app:
            self.main_app.show_login_view()

    def run(self):
        self.view.mainloop()