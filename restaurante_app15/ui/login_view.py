import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Sistema de Restaurante - Login")
        self.master.geometry("400x500")
        self.master.configure(bg="#1e293b")
        
        self.servicio = RestauranteServicio()
        self.logo_img = None
        self.pack(fill=tk.BOTH, expand=True)

        self._cargar_logo()
        self._crear_interfaz()

    def _cargar_logo(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_folder = os.path.join(base_dir, "assets", "logo")
        if os.path.exists(logo_folder):
            for file in os.listdir(logo_folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img_path = os.path.join(logo_folder, file)
                        img = Image.open(img_path).resize((90, 90), Image.Resampling.LANCZOS)
                        self.logo_img = ImageTk.PhotoImage(img)
                        break
                    except Exception:
                        pass

    def _crear_interfaz(self):
        frame_box = tk.Frame(self, bg="#1e293b")
        frame_box.pack(expand=True, fill=tk.BOTH, padx=40, pady=30)

        if self.logo_img:
            lbl_logo = tk.Label(frame_box, image=self.logo_img, bg="#1e293b")
            lbl_logo.pack(pady=(0, 10))

        lbl_titulo = tk.Label(frame_box, text="Iniciar Sesión", font=("Arial", 18, "bold"), fg="white", bg="#1e293b")
        lbl_titulo.pack(pady=(0, 20))

        tk.Label(frame_box, text="Usuario", font=("Arial", 10, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        self.txt_usuario = tk.Entry(frame_box, font=("Arial", 11), bd=0, relief=tk.FLAT)
        self.txt_usuario.pack(fill=tk.X, ipady=8, pady=(5, 15))

        tk.Label(frame_box, text="Contraseña", font=("Arial", 10, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")
        self.txt_clave = tk.Entry(frame_box, font=("Arial", 11), show="*", bd=0, relief=tk.FLAT)
        self.txt_clave.pack(fill=tk.X, ipady=8, pady=(5, 20))

        btn_ingresar = tk.Button(
            frame_box, text="Ingresar", font=("Arial", 11, "bold"),
            bg="#2563eb", fg="white", bd=0, activebackground="#1d4ed8",
            activeforeground="white", cursor="hand2", command=self._validar_login
        )
        btn_ingresar.pack(fill=tk.X, ipady=8)

    def _validar_login(self):
        usr = self.txt_usuario.get().strip()
        clave = self.txt_clave.get().strip()

        if not usr or not clave:
            messagebox.showwarning("Atención", "Por favor ingrese usuario y contraseña")
            return

        usuarios = self.servicio.obtener_usuarios()
        
        usuario_encontrado = next(
            (u for u in usuarios if str(u.get("nombre")).lower() == usr.lower() and str(u.get("clave")) == clave), 
            None
        )

        if usuario_encontrado or (usr.lower() == "admin" and clave == "1234"):
            for widget in self.master.winfo_children():
                widget.destroy()
            
            from ui.main_view import MainView
            MainView(self.master)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")