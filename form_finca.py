import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from database import obtener_conexion


class FormFinca(ctk.CTkToplevel):

  def __init__(self, parent=None):
    super().__init__(parent)

    self.title("Gestión de Fincas - Carnes de Veraguas")
    self.geometry("900x620")
    self.resizable(False, False)

    # Ventana modal sobrepuesta
    self.grab_set()

    self.crear_interfaz()
    self.mostrardatos()

  def crear_interfaz(self):
    # Título Principal
    lbl_titulo = ctk.CTkLabel(self, text="Finca", font=("Segoe UI", 20, "bold"))
    lbl_titulo.pack(pady=(15, 5))

    # --- CONTENEDOR SUPERIOR (Ingresar datos / Funciones) ---
    frame_top = ctk.CTkFrame(self, fg_color="transparent")
    frame_top.pack(fill="x", padx=20, pady=10)

    # 1. GROUPBOX: INGRESAR DATOS
    gb_datos = ctk.CTkFrame(frame_top, corner_radius=8)
    gb_datos.pack(side="left", fill="both", expand=True, padx=(0, 10))

    lbl_gb1 = ctk.CTkLabel(
        gb_datos, text="Ingresar datos", font=("Segoe UI", 12, "bold")
    )
    lbl_gb1.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)

    vcmd_num = (self.register(self.validar_solo_numeros), "%P")

    # Identificación (Prefijo "FIN" + números)
    ctk.CTkLabel(gb_datos, text="Identificación:").grid(
        row=1, column=0, sticky="e", padx=5, pady=5
    )
    frame_id = ctk.CTkFrame(gb_datos, fg_color="transparent")
    frame_id.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    lbl_prefix_fin = ctk.CTkLabel(
        frame_id, text="FIN", font=("Segoe UI", 11, "bold")
    )
    lbl_prefix_fin.pack(side="left", padx=(0, 2))

    self.tb_id = ctk.CTkEntry(
        frame_id,
        width=100,
        placeholder_text="001",
        validate="key",
        validatecommand=vcmd_num,
    )
    self.tb_id.pack(side="left")

    # Cantidad de Bovinos (Solo números)
    ctk.CTkLabel(gb_datos, text="Cantidad de Bovinos:").grid(
        row=2, column=0, sticky="e", padx=5, pady=5
    )
    self.tb_cantidad = ctk.CTkEntry(
        gb_datos, width=130, validate="key", validatecommand=vcmd_num
    )
    self.tb_cantidad.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    # Tamaño (Solo números)
    ctk.CTkLabel(gb_datos, text="Tamaño (ha²):").grid(
        row=3, column=0, sticky="e", padx=5, pady=5
    )
    self.tb_tamano = ctk.CTkEntry(
        gb_datos, width=130, validate="key", validatecommand=vcmd_num
    )
    self.tb_tamano.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    # Tipo de Terreno (Opciones fijas)
    ctk.CTkLabel(gb_datos, text="Tipo de terreno:").grid(
        row=1, column=2, sticky="e", padx=5, pady=5
    )
    self.combo_terreno = ctk.CTkComboBox(
        gb_datos,
        values=["Plano", "Ondulado", "Montañoso", "Mixto"],
        state="readonly",
        width=130,
    )
    self.combo_terreno.set("Plano")
    self.combo_terreno.grid(row=1, column=3, sticky="w", padx=5, pady=5)

    # Fuente de Agua (SI / NO)
    ctk.CTkLabel(gb_datos, text="Fuente de agua:").grid(
        row=2, column=2, sticky="e", padx=5, pady=5
    )
    self.combo_agua = ctk.CTkComboBox(
        gb_datos, values=["SI", "NO"], state="readonly", width=130
    )
    self.combo_agua.set("SI")
    self.combo_agua.grid(row=2, column=3, sticky="w", padx=5, pady=5)

    # 2. GROUPBOX: FUNCIONES (BOTONES)
    gb_funciones = ctk.CTkFrame(frame_top, corner_radius=8)
    gb_funciones.pack(side="right", fill="y", padx=(10, 0))

    lbl_gb2 = ctk.CTkLabel(
        gb_funciones, text="Funciones", font=("Segoe UI", 12, "bold")
    )
    lbl_gb2.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    btn_width = 100

    btn_insertar = ctk.CTkButton(
        gb_funciones,
        text="Insertar",
        width=btn_width,
        command=self.btnInsertarFinca_Click,
    )
    btn_insertar.grid(row=1, column=0, padx=10, pady=5)

    btn_limpiar = ctk.CTkButton(
        gb_funciones,
        text="Limpiar",
        width=btn_width,
        fg_color="#555555",
        hover_color="#333333",
        command=self.btnLimpiarFinca_Click,
    )
    btn_limpiar.grid(row=1, column=1, padx=10, pady=5)

    btn_modificar = ctk.CTkButton(
        gb_funciones,
        text="Modificar",
        width=btn_width,
        fg_color="#F57F17",
        hover_color="#E65100",
        command=self.btnModificarFinca_Click,
    )
    btn_modificar.grid(row=2, column=0, padx=10, pady=5)

    btn_consultar = ctk.CTkButton(
        gb_funciones,
        text="Consultar",
        width=btn_width,
        fg_color="#1565C0",
        hover_color="#0D47A1",
        command=self.abrir_consulta,
    )
    btn_consultar.grid(row=2, column=1, padx=10, pady=5)

    btn_eliminar = ctk.CTkButton(
        gb_funciones,
        text="Eliminar",
        width=btn_width,
        fg_color="#C62828",
        hover_color="#B71C1C",
        command=self.btnEliminarFinca_Click,
    )
    btn_eliminar.grid(row=3, column=0, padx=10, pady=5)

    btn_salir = ctk.CTkButton(
        gb_funciones,
        text="Salir",
        width=btn_width,
        fg_color="#D32F2F",
        hover_color="#9A0007",
        command=self.btnSalirFinca_Click,
    )
    btn_salir.grid(row=3, column=1, padx=10, pady=5)

    # --- CONTENEDOR INFERIOR (DATAGRIDVIEW) ---
    gb_tabla = ctk.CTkFrame(self, corner_radius=8)
    gb_tabla.pack(fill="both", expand=True, padx=20, pady=(5, 15))

    lbl_gb3 = ctk.CTkLabel(gb_tabla, text="Datos", font=("Segoe UI", 12, "bold"))
    lbl_gb3.pack(anchor="w", padx=10, pady=5)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b",
        rowheight=24,
    )
    style.configure(
        "Treeview.Heading",
        background="#1f538d",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
    )
    style.map("Treeview", background=[("selected", "#1f538d")])

    columnas = (
        "ID_Fincas",
        "Cantidad_De_Bovinos",
        "Tamano_Finca_ha2_",
        "Tipo_Terreno",
        "Fuentes_Agua",
    )
    self.dgvFinca = ttk.Treeview(
        gb_tabla, columns=columnas, show="headings", selectmode="browse"
    )

    self.dgvFinca.heading("ID_Fincas", text="ID_Fincas")
    self.dgvFinca.heading("Cantidad_De_Bovinos", text="Cantidad_De_Bovinos")
    self.dgvFinca.heading("Tamano_Finca_ha2_", text="Tamano_Finca_ha2_")
    self.dgvFinca.heading("Tipo_Terreno", text="Tipo_Terreno")
    self.dgvFinca.heading("Fuentes_Agua", text="Fuentes_Agua")

    self.dgvFinca.column("ID_Fincas", width=120, anchor="center")
    self.dgvFinca.column("Cantidad_De_Bovinos", width=140, anchor="center")
    self.dgvFinca.column("Tamano_Finca_ha2_", width=140, anchor="center")
    self.dgvFinca.column("Tipo_Terreno", width=140, anchor="w")
    self.dgvFinca.column("Fuentes_Agua", width=120, anchor="center")

    scrollbar_v = ttk.Scrollbar(
        gb_tabla, orient="vertical", command=self.dgvFinca.yview
    )
    self.dgvFinca.configure(yscrollcommand=scrollbar_v.set)

    scrollbar_v.pack(side="right", fill="y")
    self.dgvFinca.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    self.dgvFinca.bind("<<TreeviewSelect>>", self.dgvFinca_CellContentClick)

  # --- MÉTODOS Y VALIDACIONES ---

  def validar_solo_numeros(self, texto):
    return texto == "" or texto.isdigit()

  def obtener_id_completo(self):
    val = self.tb_id.get().strip()
    return f"FIN{val}" if val else ""

  def mostrardatos(self):
    for item in self.dgvFinca.get_children():
      self.dgvFinca.delete(item)

    try:
      conn = obtener_conexion()
      cursor = conn.cursor()
      cursor.execute(
          "SELECT ID_Fincas, Cantidad_De_Bovinos, Tamano_Finca_ha2_,"
          " Tipo_Terreno, Fuentes_Agua FROM TB_Fincas"
      )
      filas = cursor.fetchall()
      for fila in filas:
        self.dgvFinca.insert("", "end", values=tuple(fila))
      conn.close()
    except Exception as e:
      messagebox.showerror("Error SQL", f"Error al cargar datos: {e}")

  def dgvFinca_CellContentClick(self, event):
    seleccionado = self.dgvFinca.selection()
    if seleccionado:
      valores = self.dgvFinca.item(seleccionado, "values")

      raw_id = str(valores[0]).replace("FIN", "").strip()
      self.tb_id.delete(0, "end")
      self.tb_id.insert(0, raw_id)

      self.tb_cantidad.delete(0, "end")
      self.tb_cantidad.insert(0, valores[1])

      self.tb_tamano.delete(0, "end")
      self.tb_tamano.insert(0, valores[2])

      self.combo_terreno.set(valores[3])
      self.combo_agua.set(valores[4])

  def btnInsertarFinca_Click(self):
    id_finca = self.obtener_id_completo()
    cant_str = self.tb_cantidad.get().strip()
    tamano_str = self.tb_tamano.get().strip()

    if not self.tb_id.get().strip():
      messagebox.showwarning("Atención", "Ingrese el ID de la Finca.")
      return

    if cant_str.isdigit():
      cantidad_bovinos = int(cant_str)
      if cantidad_bovinos <= 35:
        try:
          conn = obtener_conexion()
          cursor = conn.cursor()
          sql = "INSERT INTO TB_Fincas (ID_Fincas, Cantidad_De_Bovinos, Tamano_Finca_ha2_, Tipo_Terreno, Fuentes_Agua) VALUES (?, ?, ?, ?, ?)"
          cursor.execute(
              sql,
              (
                  id_finca,
                  cantidad_bovinos,
                  int(tamano_str) if tamano_str else 0,
                  self.combo_terreno.get(),
                  self.combo_agua.get(),
              ),
          )
          conn.commit()
          conn.close()

          messagebox.showinfo("Éxito", "Datos agregados correctamente")
          self.mostrardatos()
          self.btnLimpiarFinca_Click()
        except Exception as e:
          messagebox.showerror("Error", f"Error al insertar: {e}")
      else:
        messagebox.showerror(
            "Error", "La cantidad de bovinos no puede ser superior a 35."
        )
    else:
      messagebox.showerror(
          "Error", "Ingrese un valor válido para la cantidad de bovinos."
      )

  def btnModificarFinca_Click(self):
    id_finca = self.obtener_id_completo()
    cant_str = self.tb_cantidad.get().strip()
    tamano_str = self.tb_tamano.get().strip()

    if self.tb_id.get().strip():
      if cant_str.isdigit() and int(cant_str) > 35:
        messagebox.showerror(
            "Error", "La cantidad de bovinos no puede ser superior a 35."
        )
        return

      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        sql = """UPDATE TB_Fincas SET 
                        Cantidad_De_Bovinos = ?, 
                        Tamano_Finca_ha2_ = ?, 
                        Tipo_Terreno = ?, 
                        Fuentes_Agua = ? 
                     WHERE ID_Fincas = ?"""
        cursor.execute(
            sql,
            (
                int(cant_str) if cant_str else 0,
                int(tamano_str) if tamano_str else 0,
                self.combo_terreno.get(),
                self.combo_agua.get(),
                id_finca,
            ),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Datos actualizados correctamente")
        self.mostrardatos()
        self.btnLimpiarFinca_Click()
      except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar: {e}")
    else:
      messagebox.showerror("Error", "Ingrese un ID de Finca válido")

  def btnEliminarFinca_Click(self):
    id_finca = self.obtener_id_completo()
    if not self.tb_id.get().strip():
      messagebox.showwarning("Atención", "Seleccione o ingrese un ID de finca.")
      return

    if messagebox.askyesno(
        "Confirmar", f"¿Está seguro de eliminar la finca {id_finca}?"
    ):
      try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TB_Fincas WHERE ID_Fincas = ?", (id_finca,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Datos eliminados correctamente")
        self.mostrardatos()
        self.btnLimpiarFinca_Click()
      except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar: {e}")

  def btnLimpiarFinca_Click(self):
    self.tb_id.delete(0, "end")
    self.tb_cantidad.delete(0, "end")
    self.tb_tamano.delete(0, "end")
    self.combo_terreno.set("Plano")
    self.combo_agua.set("SI")

  def btnSalirFinca_Click(self):
    self.destroy()

  def abrir_consulta(self):
    # Equivalente al Form10.Show() que tenías en VB.NET
    messagebox.showinfo("Consulta", "Abre el módulo de consultas (Form10).")


if __name__ == "__main__":
  app = ctk.CTk()
  app.geometry("400x200")
  btn = ctk.CTkButton(
      app, text="Abrir FormFinca", command=lambda: FormFinca(app)
  )
  btn.pack(expand=True)
  app.mainloop()