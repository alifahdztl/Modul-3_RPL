import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from controllers.buku_controller import BukuController

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            # Pengecekan aman untuk format dictionary atau tuple
            if isinstance(user, dict):
                nama_user = user.get('username', username)
                role = user.get('role', 'admin')
            else:
                nama_user = user[1] if len(user) > 1 else username
                role = user[3] if len(user) > 3 else (user[2] if len(user) > 2 else "admin")

            messagebox.showinfo("Login Berhasil", f"Selamat datang, {nama_user} ({role})!")
            
            # Hancurkan jendela login dengan aman
            self.view.destroy()
            
            # Buka jendela Utama Buku
            app_utama = BukuController(parent=None, main_app=self, user_role=role)
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def show_login_view(self):
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)
        self.run()

    def run(self):
        self.view.mainloop()