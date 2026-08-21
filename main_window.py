import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from form_bovino import FormBovino

# Configuración visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana inicial
        self.title("Carnes de Veraguas - Sistema Principal")
        self.geometry("1100x650")
        self.minsize(900, 500)

        # Variables para manejo de sesión
        self.usuario_actual = None
        self.rol_actual = None

        # Estado de submenús
        self.submenus_visibles = {"bovinos": False, "empleados": False, "pollos": False}

        # --- ESTRUCTURA GENERAL DE PANELS ---
        self.crear_barra_superior()
        
        # Contenedor principal inferior (Menú lateral + Área de Trabajo)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)

        self.crear_menu_lateral()
        self.crear_area_trabajo()

        # Iniciar reloj en tiempo real
        self.actualizar_reloj()

        # Ocultar botones al iniciar
        self.deshabilitar_todos_los_botones()
        
    def abrir_form2(self):
        FormBovino(self)

    # --- BARRA SUPERIOR Y RELOJ ---
    def crear_barra_superior(self):
        self.panel_top = ctk.CTkFrame(self, height=45, corner_radius=0)
        self.panel_top.pack(side="top", fill="x")

        # Título del Sistema
        lbl_titulo_app = ctk.CTkLabel(
            self.panel_top, 
            text="🥩 Carnes de Veraguas S.A.", 
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo_app.pack(side="left", padx=15)

        # Reloj y Fecha (Derecha)
        self.lbl_reloj = ctk.CTkLabel(
            self.panel_top, 
            text="", 
            font=("Segoe UI", 13, "bold")
        )
        self.lbl_reloj.pack(side="right", padx=15)

    def actualizar_reloj(self):
        ahora = datetime.datetime.now()
        hora_str = ahora.strftime("%I:%M:%S %p")
        fecha_str = ahora.strftime("%d/%m/%Y")
        self.lbl_reloj.configure(text=f"📅 {fecha_str}  |  ⏰ {hora_str}")
        self.after(1000, self.actualizar_reloj)

    # --- MENÚ LATERAL Y SUBMENÚS (ACORDEÓN) ---
    def crear_menu_lateral(self):
        self.panel_menu = ctk.CTkScrollableFrame(self.container, width=220, corner_radius=0)
        self.panel_menu.pack(side="left", fill="y")

        # Botón Iniciar Sesión / Panel Login Trigger
        self.btn_loggear = ctk.CTkButton(
            self.panel_menu, text="🔐 Iniciar Sesión", command=self.mostrar_login_panel, fg_color="#1f538d"
        )
        self.btn_loggear.pack(pady=(10, 5), padx=10, fill="x")

        # --- SECCIÓN BOVINOS ---
        self.btn_bovinos = ctk.CTkButton(
            self.panel_menu, text="🐂 Bovinos ▼", command=lambda: self.toggle_submenu("bovinos")
        )
        self.btn_bovinos.pack(pady=3, padx=10, fill="x")

        self.frame_sub_bovinos = ctk.CTkFrame(self.panel_menu, fg_color="transparent")
        self.btn_finca = ctk.CTkButton(self.frame_sub_bovinos, text="• Fincas (Form3)", command=self.abrir_form3, fg_color="#2A2D2E")
        self.btn_finca.pack(pady=2, padx=15, fill="x")
        self.btn_bovino = ctk.CTkButton(self.frame_sub_bovinos, text="• Bovino (Form2)", command=self.abrir_form2, fg_color="#2A2D2E")
        self.btn_bovino.pack(pady=2, padx=15, fill="x")
        self.btn_lote_bovino = ctk.CTkButton(self.frame_sub_bovinos, text="• Lote Bovino (Form4)", command=self.abrir_form4, fg_color="#2A2D2E")
        self.btn_lote_bovino.pack(pady=2, padx=15, fill="x")
        self.btn_bovino1 = ctk.CTkButton(self.frame_sub_bovinos, text="👁 Solo Ver Bovinos", command=self.abrir_ver_bovinos, fg_color="#1C3829")
        self.btn_bovino1.pack(pady=2, padx=15, fill="x")

        # --- SECCIÓN EMPLEADOS E INSUMOS ---
        self.btn_empleados = ctk.CTkButton(
            self.panel_menu, text="👥 Empleados e Insumos ▼", command=lambda: self.toggle_submenu("empleados")
        )
        self.btn_empleados.pack(pady=3, padx=10, fill="x")

        self.frame_sub_empleados = ctk.CTkFrame(self.panel_menu, fg_color="transparent")
        self.btn_empleado_form = ctk.CTkButton(self.frame_sub_empleados, text="• Empleados (Form5)", command=self.abrir_form5, fg_color="#2A2D2E")
        self.btn_empleado_form.pack(pady=2, padx=15, fill="x")
        self.btn_insumos = ctk.CTkButton(self.frame_sub_empleados, text="• Insumos (Form8)", command=self.abrir_form8, fg_color="#2A2D2E")
        self.btn_insumos.pack(pady=2, padx=15, fill="x")

        # --- SECCIÓN POLLOS ---
        self.btn_pollos = ctk.CTkButton(
            self.panel_menu, text="🐔 Pollos / Aves ▼", command=lambda: self.toggle_submenu("pollos")
        )
        self.btn_pollos.pack(pady=3, padx=10, fill="x")

        self.frame_sub_pollos = ctk.CTkFrame(self.panel_menu, fg_color="transparent")
        self.btn_galera = ctk.CTkButton(self.frame_sub_pollos, text="• Galeras (Form6)", command=self.abrir_form6, fg_color="#2A2D2E")
        self.btn_galera.pack(pady=2, padx=15, fill="x")
        self.btn_lote_ave = ctk.CTkButton(self.frame_sub_pollos, text="• Lotes Aves (Form7)", command=self.abrir_form7, fg_color="#2A2D2E")
        self.btn_lote_ave.pack(pady=2, padx=15, fill="x")
        self.btn_pollo1 = ctk.CTkButton(self.frame_sub_pollos, text="👁 Solo Ver Pollos", command=self.abrir_ver_pollos, fg_color="#1C3829")
        self.btn_pollo1.pack(pady=2, padx=15, fill="x")

        # Botón Guía de Usuario
        self.btn_guia = ctk.CTkButton(self.panel_menu, text="❓ Guía de Usuario", command=self.mostrar_guia, fg_color="#5B5B5B")
        self.btn_guia.pack(pady=(15, 5), padx=10, fill="x")

        # Botón Salir / Cerrar Sesión
        self.btn_salir = ctk.CTkButton(self.panel_menu, text="🚪 Cerrar Sesión", command=self.cerrar_sesion, fg_color="#900C3F")
        self.btn_salir.pack(pady=5, padx=10, fill="x")

    def toggle_submenu(self, nombre):
        frame_map = {
            "bovinos": self.frame_sub_bovinos,
            "empleados": self.frame_sub_empleados,
            "pollos": self.frame_sub_pollos
        }
        
        # Ocultar todos primero
        for clave, frame in frame_map.items():
            if clave != nombre:
                frame.pack_forget()
                self.submenus_visibles[clave] = False

        # Alternar el seleccionado
        if self.submenus_visibles[nombre]:
            frame_map[nombre].pack_forget()
            self.submenus_visibles[nombre] = False
        else:
            frame_map[nombre].pack(fill="x", after=getattr(self, f"btn_{nombre}"))
            self.submenus_visibles[nombre] = True

    # --- ÁREA CENTRAL / FORMULARIO DE LOGIN ---
    def crear_area_trabajo(self):
        self.area_principal = ctk.CTkFrame(self.container, corner_radius=10)
        self.area_principal.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Panel de Inicio de Sesión
        self.panel_login = ctk.CTkFrame(self.area_principal, corner_radius=10, width=320, height=350)
        
        lbl_login_title = ctk.CTkLabel(self.panel_login, text="Control de Acceso", font=("Segoe UI", 18, "bold"))
        lbl_login_title.pack(pady=20)

        self.tb_usuario = ctk.CTkEntry(self.panel_login, placeholder_text="Usuario", width=220)
        self.tb_usuario.pack(pady=10)
        self.tb_usuario.bind("<Return>", lambda e: self.tb_clave.focus())

        self.tb_clave = ctk.CTkEntry(self.panel_login, placeholder_text="Contraseña", show="*", width=220)
        self.tb_clave.pack(pady=10)
        self.tb_clave.bind("<Return>", lambda e: self.procesar_login())

        self.bt_entrar = ctk.CTkButton(self.panel_login, text="Entrar", command=self.procesar_login, width=220)
        self.bt_entrar.pack(pady=20)

    def mostrar_login_panel(self):
        self.panel_login.place(relx=0.5, rely=0.5, anchor="center")

    def ocultar_login_panel(self):
        self.panel_login.place_forget()

    # --- LÓGICA DE CONTROL DE ACCESO (LOGIN) ---
    def procesar_login(self):
        user_in = self.tb_usuario.get().strip()
        pass_in = self.tb_clave.get().strip()

        # Validación temporal exacta según tu VB
        if user_in == "Admin" and pass_in == "1234":
            messagebox.showinfo("Acceso", "Bienvenido Admin")
            self.habilitar_todos_los_botones()
            self.ocultar_login_panel()
        elif user_in == "empleado1" and pass_in == "12345":
            messagebox.showinfo("Acceso", "Bienvenido Empleado 1")
            self.deshabilitar_todos_los_botones()
            self.btn_bovino1.configure(state="normal")
            self.btn_salir.configure(state="normal")
            self.ocultar_login_panel()
        elif user_in == "empleado2" and pass_in == "123456":
            messagebox.showinfo("Acceso", "Bienvenido Empleado 2")
            self.deshabilitar_todos_los_botones()
            self.btn_pollo1.configure(state="normal")
            self.btn_salir.configure(state="normal")
            self.ocultar_login_panel()
        else:
            messagebox.showerror("Error", "Algo está mal, revisa el usuario o contraseña")
            self.tb_usuario.delete(0, "end")
            self.tb_clave.delete(0, "end")
            self.deshabilitar_todos_los_botones()

    def habilitar_todos_los_botones(self):
        botones = [
            self.btn_bovinos, self.btn_empleados, self.btn_pollos, self.btn_salir,
            self.btn_finca, self.btn_bovino, self.btn_lote_bovino, self.btn_bovino1,
            self.btn_empleado_form, self.btn_insumos, self.btn_galera, self.btn_lote_ave, self.btn_pollo1
        ]
        for btn in botones:
            btn.configure(state="normal")
        self.btn_loggear.configure(state="disabled")

    def deshabilitar_todos_los_botones(self):
        botones = [
            self.btn_bovinos, self.btn_empleados, self.btn_pollos, self.btn_salir,
            self.btn_finca, self.btn_bovino, self.btn_lote_bovino, self.btn_bovino1,
            self.btn_empleado_form, self.btn_insumos, self.btn_galera, self.btn_lote_ave, self.btn_pollo1
        ]
        for btn in botones:
            btn.configure(state="disabled")
        self.btn_loggear.configure(state="normal")

    def cerrar_sesion(self):
        messagebox.showinfo("Despedida", "Hasta luego usuario tenga un buen día")
        self.deshabilitar_todos_los_botones()
        self.tb_usuario.delete(0, "end")
        self.tb_clave.delete(0, "end")
        self.mostrar_login_panel()

    def mostrar_guia(self):
        info = ("Primero debes iniciar sesión con tu Usuario y Clave\n"
                "luego tendrás opciones de visualización y edición de datos para lo almacenado en la DataBase")
        messagebox.showinfo("Información", info)

    # --- MÉTODOS PARA ABRIR SUBFORMULARIOS ---
    #def abrir_form2(self): messagebox.showinfo("Módulo", "Abriendo Form2 (Bovinos)...")
    def abrir_form3(self): messagebox.showinfo("Módulo", "Abriendo Form3 (Fincas)...")
    def abrir_form4(self): messagebox.showinfo("Módulo", "Abriendo Form4 (Lote Bovinos)...")
    def abrir_form5(self): messagebox.showinfo("Módulo", "Abriendo Form5 (Empleados)...")
    def abrir_form6(self): messagebox.showinfo("Módulo", "Abriendo Form6 (Galeras)...")
    def abrir_form7(self): messagebox.showinfo("Módulo", "Abriendo Form7 (Lote Aves)...")
    def abrir_form8(self): messagebox.showinfo("Módulo", "Abriendo Form8 (Insumos)...")
    def abrir_ver_bovinos(self): messagebox.showinfo("Módulo", "Abriendo FormSoloVerBovino...")
    def abrir_ver_pollos(self): messagebox.showinfo("Módulo", "Abriendo FormSoloVerPollos...")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()