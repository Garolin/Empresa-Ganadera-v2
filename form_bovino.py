import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pyodbc
from database import obtener_conexion  # Importa la función de conexión desde database.py

class FormBovino(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Gestión de Bovinos - Carnes de Veraguas")
        self.geometry("1100x700")
        self.minsize(950, 600)

        # Hacer que la ventana se sobreponga
        self.grab_set()

        # --- ESTRUCTURA GENERAL ---
        self.crear_interfaz()
        self.mostrar_datos()

    def crear_interfaz(self):
        # Título Superior
        lbl_titulo = ctk.CTkLabel(self, text="🐄 Módulo de Gestión de Bovinos", font=("Segoe UI", 20, "bold"))
        lbl_titulo.pack(pady=15)

        # Contenedor divido: Izquierda (Campos y Botones) / Derecha (Tabla DataGridView)
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- PANEL IZQUIERDO: FORMULARIO ---
        self.frame_inputs = ctk.CTkFrame(self.main_container, width=320)
        self.frame_inputs.pack(side="left", fill="y", padx=10, pady=10)

        lbl_sub = ctk.CTkLabel(self.frame_inputs, text="Datos del Bovino", font=("Segoe UI", 14, "bold"))
        lbl_sub.pack(pady=10)

        # Entradas de texto (Campos)
        self.tb_id = ctk.CTkEntry(self.frame_inputs, placeholder_text="ID Bovino", width=250)
        self.tb_id.pack(pady=5)

        self.tb_raza = ctk.CTkEntry(self.frame_inputs, placeholder_text="Raza", width=250)
        self.tb_raza.pack(pady=5)

        self.tb_peso = ctk.CTkEntry(self.frame_inputs, placeholder_text="Peso (kg/lbs)", width=250)
        self.tb_peso.pack(pady=5)

        self.tb_sexo = ctk.CTkEntry(self.frame_inputs, placeholder_text="Sexo (M/F)", width=250)
        self.tb_sexo.pack(pady=5)

        self.tb_edad = ctk.CTkEntry(self.frame_inputs, placeholder_text="Edad (Meses)", width=250)
        self.tb_edad.pack(pady=5)

        self.tb_status = ctk.CTkEntry(self.frame_inputs, placeholder_text="Estatus", width=250)
        self.tb_status.pack(pady=5)

        self.tb_lote = ctk.CTkEntry(self.frame_inputs, placeholder_text="ID Lote", width=250)
        self.tb_lote.pack(pady=5)

        # --- BOTONES DE ACCIÓN CRUD ---
        self.frame_botones = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_botones.pack(pady=15, fill="x", padx=10)

        btn_insertar = ctk.CTkButton(self.frame_botones, text="➕ Insertar", command=self.insertar_bovino, fg_color="#2E7D32", width=110)
        btn_insertar.grid(row=0, column=0, padx=5, pady=5)

        btn_modificar = ctk.CTkButton(self.frame_botones, text="✏️ Modificar", command=self.modificar_bovino, fg_color="#F57F17", width=110)
        btn_modificar.grid(row=0, column=1, padx=5, pady=5)

        btn_eliminar = ctk.CTkButton(self.frame_botones, text="🗑️ Eliminar", command=self.eliminar_bovino, fg_color="#C62828", width=110)
        btn_eliminar.grid(row=1, column=0, padx=5, pady=5)

        btn_limpiar = ctk.CTkButton(self.frame_botones, text="🧹 Limpiar", command=self.limpiar_campos, fg_color="#555555", width=110)
        btn_limpiar.grid(row=1, column=1, padx=5, pady=5)

        # --- BOTONES DE FUNCIONES ESPECIALES Y PROCEDIMIENTOS ---
        btn_actualizar_sp = ctk.CTkButton(self.frame_inputs, text="⚙️ Actualizar Estado (SP)", command=self.ejecutar_sp_actualizar, fg_color="#1565C0", width=230)
        btn_actualizar_sp.pack(pady=5)

        btn_promedio_func = ctk.CTkButton(self.frame_inputs, text="📊 Ver Peso Promedio y Predominio", command=self.ejecutar_funcion_promedio, fg_color="#6A1B9A", width=230)
        btn_promedio_func.pack(pady=5)

        # --- PANEL DERECHO: DATAGRIDVIEW (Treeview) ---
        self.frame_tabla = ctk.CTkFrame(self.main_container)
        self.frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=25)
        style.configure("Treeview.Heading", background="#1f1f1f", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#1f538d")])

        columnas = ("ID", "Raza", "Peso", "Sexo", "Edad (Meses)", "Status", "ID Lote")
        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings", selectmode="browse")

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor="center")

        # Scrollbar vertical para la tabla
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento Doble Clic en celda (Cargar campos)
        self.tree.bind("<Double-1>", self.al_doble_clic)

    # --- LÓGICA DE BASE DE DATOS ---

    def mostrar_datos(self):
        """Carga todos los registros de TB_Bovinos a la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT ID_Bovino, Raza_Bovino, Peso_Bovino, Sexo_Bovino, Edad_Meses_Bovino, Status_Bovino, ID_Lote_Bovinos FROM TB_Bovinos")
            filas = cursor.fetchall()
            for fila in filas:
                self.tree.insert("", "end", values=tuple(fila))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error SQL", f"Error al cargar datos: {e}")

    def al_doble_clic(self, event):
        """Llena los campos de entrada al hacer doble clic en una fila."""
        item = self.tree.selection()
        if not item:
            return
        valores = self.tree.item(item[0], "values")

        self.limpiar_campos()
        self.tb_id.insert(0, valores[0])
        self.tb_raza.insert(0, valores[1])
        self.tb_peso.insert(0, valores[2])
        self.tb_sexo.insert(0, valores[3])
        self.tb_edad.insert(0, valores[4])
        self.tb_status.insert(0, valores[5])
        self.tb_lote.insert(0, valores[6])

    def insertar_bovino(self):
        """Insertar usando parámetros seguros en lugar de concatenación SQL."""
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO TB_Bovinos (ID_Bovino, Raza_Bovino, Peso_Bovino, Sexo_Bovino, Edad_Meses_Bovino, Status_Bovino, ID_Lote_Bovinos) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)"""
            valores = (
                self.tb_id.get().strip(),
                self.tb_raza.get().strip(),
                self.tb_peso.get().strip(),
                self.tb_sexo.get().strip(),
                self.tb_edad.get().strip(),
                self.tb_status.get().strip(),
                self.tb_lote.get().strip()
            )
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos agregados correctamente")
            self.mostrar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error al Insertar", f"Error al insertar datos: {e}")

    def modificar_bovino(self):
        """Actualizar datos usando consultas parametrizadas."""
        id_bovino = self.tb_id.get().strip()
        if not id_bovino:
            messagebox.showwarning("Atención", "Ingrese un ID de Bovino válido")
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            sql = """UPDATE TB_Bovinos SET 
                        Raza_Bovino = ?, 
                        Peso_Bovino = ?, 
                        Sexo_Bovino = ?, 
                        Edad_Meses_Bovino = ?, 
                        Status_Bovino = ?, 
                        ID_Lote_Bovinos = ?
                     WHERE ID_Bovino = ?"""
            valores = (
                self.tb_raza.get().strip(),
                self.tb_peso.get().strip(),
                self.tb_sexo.get().strip(),
                self.tb_edad.get().strip(),
                self.tb_status.get().strip(),
                self.tb_lote.get().strip(),
                id_bovino
            )
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos actualizados correctamente")
            self.mostrar_datos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error al Actualizar", f"Error al actualizar datos: {e}")

    def eliminar_bovino(self):
        """Eliminar un registro por ID."""
        id_bovino = self.tb_id.get().strip()
        if not id_bovino:
            messagebox.showwarning("Atención", "Seleccione o ingrese el ID a eliminar")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el bovino {id_bovino}?"):
            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM TB_Bovinos WHERE ID_Bovino = ?", (id_bovino,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Datos eliminados correctamente")
                self.mostrar_datos()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error al Eliminar", f"Error al eliminar: {e}")

    def ejecutar_sp_actualizar(self):
        """Ejecuta el Procedimiento Almacenado 'ActualizarEstadoBovinos'."""
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("{CALL ActualizarEstadoBovinos}")
            conn.commit()
            conn.close()

            messagebox.showinfo("Procedimiento Almacenado", "Estado de bovinos actualizado correctamente")
            self.mostrar_datos()
        except Exception as e:
            messagebox.showerror("Error SP", f"Error al actualizar el estado de bovinos: {e}")

    def ejecutar_funcion_promedio(self):
        """Ejecuta la Función de Tabla 'CalcularPesoPromedioGanadoConPredominio()'."""
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CalcularPesoPromedioGanadoConPredominio()")
            row = cursor.fetchone()
            conn.close()

            if row:
                peso_promedio = row[0]
                total_bovinos = row[1]
                cant_machos = row[2]
                cant_hembras = row[3]
                predominio = row[4]

                res = (
                    f"Peso Promedio: {peso_promedio}\n"
                    f"Total de Bovinos: {total_bovinos}\n"
                    f"Cantidad de Machos: {cant_machos}\n"
                    f"Cantidad de Hembras: {cant_hembras}\n"
                    f"Predominio Sexo: {predominio}"
                )
                messagebox.showinfo("Resultados", res)
            else:
                messagebox.showwarning("Sin Datos", "No se encontraron resultados.")
        except Exception as e:
            messagebox.showerror("Error Función", f"Error al obtener los resultados: {e}")

    def limpiar_campos(self):
        """Limpia los campos del formulario."""
        self.tb_id.delete(0, "end")
        self.tb_raza.delete(0, "end")
        self.tb_peso.delete(0, "end")
        self.tb_sexo.delete(0, "end")
        self.tb_edad.delete(0, "end")
        self.tb_status.delete(0, "end")
        self.tb_lote.delete(0, "end")


if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()  # Oculta la ventana principal solo para probar el FormBovino
    app = FormBovino()
    app.mainloop()