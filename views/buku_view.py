import customtkinter as ctk
from tkinter import ttk
import tkinter.messagebox as messagebox

class BukuView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Ambil role dari controller untuk menentukan judul/hak akses
        role_teks = str(self.controller.user_role).upper() if hasattr(self.controller, 'user_role') and self.controller.user_role else "ADMIN"
        self.title(f"Sistem Manajemen Perpustakaan - Mode: {role_teks}")
        self.geometry("900x600")
        
        self.init_ui()

    def init_ui(self):
        # Frame Kiri (Form Input)
        left_frame = ctk.CTkFrame(self, width=350)
        left_frame.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(left_frame, text="Form Data Buku", font=("Arial", 18, "bold")).pack(pady=15)

        self.entry_judul = ctk.CTkEntry(left_frame, placeholder_text="Masukkan Judul Buku", width=280)
        self.entry_judul.pack(pady=10)

        self.entry_penulis = ctk.CTkEntry(left_frame, placeholder_text="Masukkan Nama Penulis", width=280)
        self.entry_penulis.pack(pady=10)

        self.entry_tahun = ctk.CTkEntry(left_frame, placeholder_text="Tahun Terbit (Misal: 2024)", width=280)
        self.entry_tahun.pack(pady=10)

        # Cek apakah user adalah anggota
        is_anggota = hasattr(self.controller, 'user_role') and str(self.controller.user_role).lower() in ['anggota', 'member', 'user']

        if is_anggota:
            # Mode Anggota: Teks sesuai modul (Akses Terkunci, Update Data, Hapus Data) tapi TETAP BERWARNA (hijau, kuning, merah)
            btn_simpan = ctk.CTkButton(left_frame, text="Akses Terkunci (Khusus Admin)", fg_color="green", hover_color="darkgreen", 
                                       command=lambda: messagebox.showwarning("Akses Dibatasi", "Fitur ini khusus untuk Admin!"))
            btn_simpan.pack(pady=10, fill="x")

            btn_update = ctk.CTkButton(left_frame, text="Update Data", fg_color="orange", hover_color="darkorange", 
                                       command=lambda: messagebox.showwarning("Akses Dibatasi", "Update data khusus untuk Admin!"))
            btn_update.pack(pady=10, fill="x")

            btn_hapus = ctk.CTkButton(left_frame, text="Hapus Data", fg_color="red", hover_color="darkred", 
                                       command=lambda: messagebox.showwarning("Akses Dibatasi", "Hapus data khusus untuk Admin!"))
            btn_hapus.pack(pady=10, fill="x")
            
            # Nonaktifkan input form agar anggota tidak bisa mengetik
            self.entry_judul.configure(state="disabled")
            self.entry_penulis.configure(state="disabled")
            self.entry_tahun.configure(state="disabled")
        else:
            # Mode Admin: Tombol aktif dan berfungsi normal
            btn_simpan = ctk.CTkButton(left_frame, text="Simpan Data", fg_color="green", hover_color="darkgreen", command=self.controller.tambah_buku_action)
            btn_simpan.pack(pady=10, fill="x")

            btn_update = ctk.CTkButton(left_frame, text="Perbarui Data (Update)", fg_color="orange", hover_color="darkorange", command=self.controller.update_buku_action)
            btn_update.pack(pady=10, fill="x")

            btn_hapus = ctk.CTkButton(left_frame, text="Hapus Data (Delete)", fg_color="red", hover_color="darkred", command=self.controller.hapus_buku_action)
            btn_hapus.pack(pady=10, fill="x")

        btn_logout = ctk.CTkButton(left_frame, text="Logout", fg_color="gray", hover_color="darkgray", command=self.controller.logout)
        btn_logout.pack(pady=30, fill="x")

        # Frame Kanan (Tabel Daftar Buku)
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(right_frame, text="Daftar Koleksi Buku", font=("Arial", 18, "bold")).pack(pady=15)

        # Tabel Treeview
        columns = ("id", "judul", "penulis", "tahun")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("judul", text="Judul Buku")
        self.tree.heading("penulis", text="Penulis")
        self.tree.heading("tahun", text="Tahun")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("judul", width=200)
        self.tree.column("penulis", width=150)
        self.tree.column("tahun", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Event Binding
        self.tree.bind('<<TreeviewSelect>>', self.controller.pilih_buku_action)