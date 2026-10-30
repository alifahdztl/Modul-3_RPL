import customtkinter as ctk
from tkinter import ttk

class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("860x520")
        self.resizable(False, False)

        # Mengatur tema tampilan (mengikuti sistem/default)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Container Utama
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=15, padx=15, fill="both", expand=True)

        # --- FRAME FORM INPUT (KIRI) ---
        self.frame_form = ctk.CTkFrame(self.main_frame, width=320)
        self.frame_form.pack(side="left", fill="y", padx=10, pady=10)

        lbl_form = ctk.CTkLabel(self.frame_form, text="Form Data Buku", font=("Arial", 16, "bold"))
        lbl_form.pack(pady=(20, 15))

        self.entry_judul = ctk.CTkEntry(self.frame_form, placeholder_text="Masukkan Judul Buku", width=270, height=35)
        self.entry_judul.pack(pady=10, padx=15)

        self.entry_penulis = ctk.CTkEntry(self.frame_form, placeholder_text="Masukkan Nama Penulis", width=270, height=35)
        self.entry_penulis.pack(pady=10, padx=15)

        self.entry_tahun = ctk.CTkEntry(self.frame_form, placeholder_text="Tahun Terbit (Misal: 2024)", width=270, height=35)
        self.entry_tahun.pack(pady=10, padx=15)

        # Tombol-tombol Aksi dengan CustomTkinter
        self.btn_simpan = ctk.CTkButton(self.frame_form, text="Simpan Data", fg_color="green", hover_color="darkgreen", width=270, height=35)
        self.btn_simpan.pack(pady=8, padx=15)

        self.btn_update = ctk.CTkButton(self.frame_form, text="Perbarui Data (Update)", fg_color="orange", hover_color="darkorange", text_color="black", width=270, height=35)
        self.btn_update.pack(pady=8, padx=15)

        self.btn_delete = ctk.CTkButton(self.frame_form, text="Hapus Data (Delete)", fg_color="red", hover_color="darkred", width=270, height=35)
        self.btn_delete.pack(pady=8, padx=15)

        self.btn_logout = ctk.CTkButton(self.frame_form, text="Logout", fg_color="gray", hover_color="darkgray", width=270, height=35)
        self.btn_logout.pack(pady=(20, 15), padx=15)

        # --- FRAME TABEL DAFTAR BUKU (KANAN) ---
        self.frame_tabel = ctk.CTkFrame(self.main_frame)
        self.frame_tabel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        lbl_tabel = ctk.CTkLabel(self.frame_tabel, text="Daftar Koleksi Buku", font=("Arial", 16, "bold"))
        lbl_tabel.pack(pady=(20, 15))

        # Wadah tabel agar menyatu dengan gaya modern
        table_container = ctk.CTkFrame(self.frame_tabel)
        table_container.pack(fill="both", expand=True, padx=15, pady=(0, 20))

        columns = ("id_buku", "judul", "penulis", "tahun")
        self.tabel = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        
        self.tabel.heading("id_buku", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")
        
        self.tabel.column("id_buku", width=40, anchor="center")
        self.tabel.column("judul", width=160)
        self.tabel.column("penulis", width=140)
        self.tabel.column("tahun", width=60, anchor="center")
        
        self.tabel.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Scrollbar tabel
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tabel.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabel.configure(yscrollcommand=scrollbar.set)