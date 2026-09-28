import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Restaurante - Panel Principal")
        self.master.geometry("950x600")

        self.servicio = RestauranteServicio()
        self.imagenes = {}

        self.color_sidebar = "#1e293b"
        self.color_activo = "#2563eb"
        self.color_fondo = "#f8fafc"
        self.color_texto = "#334155"

        self.master.configure(bg=self.color_fondo)
        self.pack(fill=tk.BOTH, expand=True)

        self._cargar_recursos_assets()
        self._crear_interfaz()
        self.mostrar_seccion_inicio()

    def _cargar_recursos_assets(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_assets = os.path.join(base_dir, "assets")

        icon_files = {
            "home": "icons/home.png",
            "users": "icons/users.png",
            "products": "icons/products.png",
            "sales": "icons/sales.png",
            "logout": "icons/logout.png",
            "add": "icons/add.png",
            "pdf": "icons/pdf.png"
        }

        for key, rel_path in icon_files.items():
            full_path = os.path.join(path_assets, rel_path)
            if os.path.exists(full_path):
                try:
                    img = Image.open(full_path).resize((18, 18), Image.Resampling.LANCZOS)
                    self.imagenes[key] = ImageTk.PhotoImage(img)
                except Exception:
                    self.imagenes[key] = None
            else:
                self.imagenes[key] = None

        # Carga opcional del logo si existe en assets/logo
        logo_folder = os.path.join(path_assets, "logo")
        self.imagenes["logo_inicio"] = None
        if os.path.exists(logo_folder):
            for file in os.listdir(logo_folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(os.path.join(logo_folder, file)).resize((100, 100), Image.Resampling.LANCZOS)
                        self.imagenes["logo_inicio"] = ImageTk.PhotoImage(img)
                        break
                    except Exception:
                        pass

    def _crear_interfaz(self):
        self.sidebar = tk.Frame(self, bg=self.color_sidebar, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        lbl_brand = tk.Label(self.sidebar, text="RESTAURANTE", fg="white", bg=self.color_sidebar, font=("Arial", 16, "bold"))
        lbl_brand.pack(anchor="w", padx=20, pady=(20, 2))

        lbl_role = tk.Label(self.sidebar, text="Administrador", fg="#94a3b8", bg=self.color_sidebar, font=("Arial", 9))
        lbl_role.pack(anchor="w", padx=20, pady=(0, 20))

        self.btn_inicio = self._crear_boton_sidebar("Inicio", self.imagenes.get("home"), self.mostrar_seccion_inicio)
        self.btn_usuarios = self._crear_boton_sidebar("Usuarios", self.imagenes.get("users"), self.mostrar_seccion_usuarios)
        self.btn_productos = self._crear_boton_sidebar("Productos", self.imagenes.get("products"), self.mostrar_seccion_productos)
        self.btn_ventas = self._crear_boton_sidebar("Ventas", self.imagenes.get("sales"), self.mostrar_seccion_ventas)

        btn_logout = tk.Button(self.sidebar, text="  Cerrar sesión", image=self.imagenes.get("logout"),
                               compound=tk.LEFT, bg="#e11d48", fg="white", font=("Arial", 10, "bold"),
                               bd=0, anchor="w", padx=15, pady=10, cursor="hand2", command=self._cerrar_sesion)
        btn_logout.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)

        self.contenido = tk.Frame(self, bg=self.color_fondo)
        self.contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)

        self.statusBar = tk.Frame(self, bg="#e2e8f0", height=25)
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbl_status = tk.Label(self.statusBar, text="", bg="#e2e8f0", fg="#475569", font=("Arial", 9))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

    def _crear_boton_sidebar(self, texto, icono, comando):
        btn = tk.Button(self.sidebar, text=f"  {texto}", image=icono, compound=tk.LEFT,
                        bg=self.color_sidebar, fg="white", font=("Arial", 10, "normal"),
                        bd=0, anchor="w", padx=20, pady=10, command=comando, cursor="hand2")
        btn.pack(fill=tk.X, pady=2)
        return btn

    def _resaltar_boton_activo(self, boton_activo):
        for btn in [self.btn_inicio, self.btn_usuarios, self.btn_productos, self.btn_ventas]:
            btn.config(bg=self.color_sidebar, font=("Arial", 10, "normal"))
        boton_activo.config(bg=self.color_activo, font=("Arial", 10, "bold"))

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_seccion_inicio(self):
        self._limpiar_contenido()
        self._resaltar_boton_activo(self.btn_inicio)

        frame_welcome = tk.Frame(self.contenido, bg=self.color_fondo)
        frame_welcome.pack(anchor="w", pady=20)

        if self.imagenes.get("logo_inicio"):
            lbl_img = tk.Label(frame_welcome, image=self.imagenes["logo_inicio"], bg=self.color_fondo)
            lbl_img.pack(side=tk.LEFT, padx=(0, 20))

        frame_texto = tk.Frame(frame_welcome, bg=self.color_fondo)
        frame_texto.pack(side=tk.LEFT)

        tk.Label(frame_texto, text="Bienvenido al Sistema", font=("Arial", 22, "bold"),
                 bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 5))
        
        tk.Label(frame_texto, text="Seleccione una opción del menú lateral para comenzar a gestionar el restaurante.",
                 font=("Arial", 11), bg=self.color_fondo, fg="#64748b").pack(anchor="w")

    def mostrar_seccion_usuarios(self):
        self._limpiar_contenido()
        self._resaltar_boton_activo(self.btn_usuarios)

        tk.Label(self.contenido, text="Gestión de Usuarios", font=("Arial", 22, "bold"),
                 bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 15))

        tabla = ttk.Treeview(self.contenido, columns=("ID", "Nombre", "Rol"), show="headings")
        tabla.heading("ID", text="ID")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Rol", text="Rol")
        tabla.pack(fill=tk.BOTH, expand=True)

        for u in self.servicio.obtener_usuarios():
            tabla.insert("", tk.END, values=(u.get("id"), u.get("nombre"), u.get("rol", "Cliente")))

    def mostrar_seccion_productos(self):
        self._limpiar_contenido()
        self._resaltar_boton_activo(self.btn_productos)

        tk.Label(self.contenido, text="Gestión de Productos", font=("Arial", 22, "bold"),
                 bg=self.color_fondo, fg=self.color_texto).pack(anchor="w", pady=(0, 15))

        tabla = ttk.Treeview(self.contenido, columns=("ID", "Nombre", "Precio"), show="headings")
        tabla.heading("ID", text="ID")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Precio", text="Precio")
        tabla.pack(fill=tk.BOTH, expand=True)

        for p in self.servicio.obtener_productos():
            tabla.insert("", tk.END, values=(p.get("id"), p.get("nombre"), f"${p.get('precio', 0)}"))

    def mostrar_seccion_ventas(self):
        self._limpiar_contenido()
        self._resaltar_boton_activo(self.btn_ventas)

        lbl_titulo = tk.Label(self.contenido, text="Ventas", font=("Arial", 22, "bold"),
                              bg=self.color_fondo, fg=self.color_texto)
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        grid_frame = tk.Frame(self.contenido, bg=self.color_fondo)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        frame_form = tk.LabelFrame(grid_frame, text="Registrar venta", font=("Arial", 10, "bold"),
                                   bg=self.color_fondo, fg=self.color_texto, padx=15, pady=15)
        frame_form.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), anchor="n")

        tk.Label(frame_form, text="Usuario", bg=self.color_fondo, font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.combo_usuarios = ttk.Combobox(frame_form, state="readonly", width=22)
        self.combo_usuarios.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame_form, text="Producto", bg=self.color_fondo, font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.combo_productos = ttk.Combobox(frame_form, state="readonly", width=22)
        self.combo_productos.grid(row=1, column=1, padx=10, pady=10)

        btn_registrar = tk.Button(
            frame_form, 
            text="  Registrar venta", 
            image=self.imagenes.get("add"), 
            compound=tk.LEFT,
            bg=self.color_activo, 
            fg="white", 
            font=("Arial", 10, "bold"), 
            bd=0, 
            pady=8,
            command=self._callback_registrar_venta,
            cursor="hand2"
        )
        btn_registrar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 8))

        btn_pdf = tk.Button(
            frame_form, 
            text="  Generar reporte PDF", 
            image=self.imagenes.get("pdf"), 
            compound=tk.LEFT,
            bg="#0f172a", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            bd=0, 
            pady=8,
            command=self._callback_generar_pdf,
            cursor="hand2"
        )
        btn_pdf.grid(row=3, column=0, columnspan=2, sticky="ew", pady=4)

        frame_tabla = tk.LabelFrame(grid_frame, text="Ventas registradas", font=("Arial", 10, "bold"),
                                    bg=self.color_fondo, fg=self.color_texto, padx=10, pady=10)
        frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columnas = ("Venta", "Usuario", "Producto")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        
        self.tree.heading("Venta", text="Venta")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Producto", text="Producto")
        
        self.tree.column("Venta", width=70, anchor="center")
        self.tree.column("Usuario", width=150, anchor="w")
        self.tree.column("Producto", width=150, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._cargar_comboboxes()
        self._actualizar_tabla_ventas()

    def _cargar_comboboxes(self):
        self.map_usuarios = {f"{u.get('id')} - {u.get('nombre', 'Usuario')}": u.get('id') 
                             for u in self.servicio.obtener_usuarios()}
        self.map_productos = {f"{p.get('nombre')} (${p.get('precio', 0)})": p.get('id') 
                              for p in self.servicio.obtener_productos()}

        self.combo_usuarios['values'] = list(self.map_usuarios.keys())
        self.combo_productos['values'] = list(self.map_productos.keys())

    def _callback_registrar_venta(self):
        usr_key = self.combo_usuarios.get()
        prod_key = self.combo_productos.get()

        id_usuario = self.map_usuarios.get(usr_key)
        id_producto = self.map_productos.get(prod_key)

        exito, mensaje = self.servicio.registrar_venta(id_usuario, id_producto)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.combo_usuarios.set('')
            self.combo_productos.set('')
            self._actualizar_tabla_ventas()
        else:
            messagebox.showwarning("Atención", mensaje)

    def _actualizar_tabla_ventas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        ventas = self.servicio.obtener_ventas()
        for v in ventas:
            prod_nombre = getattr(v, 'nombre_producto', 'Producto')
            self.tree.insert("", tk.END, values=(v.id_venta, v.nombre_usuario, prod_nombre))

        cant_prod = len(self.servicio.obtener_productos())
        cant_usr = len(self.servicio.obtener_usuarios())
        cant_ventas = len(ventas)
        self.lbl_status.config(text=f"Productos: {cant_prod} | Usuarios: {cant_usr} | Ventas: {cant_ventas} | Datos JSON locales")

    def _cerrar_sesion(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from ui.login_view import LoginView
        self.master.geometry("400x500")
        LoginView(self.master)

    def _callback_generar_pdf(self):
        exito, mensaje = self.servicio.generar_reporte_pdf()
        if exito:
            messagebox.showinfo("Reporte Creado", mensaje)
        else:
            messagebox.showwarning("Atención", mensaje)