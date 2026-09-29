import sqlite3
import tkinter as tk
from tkinter import messagebox

# ============================================================
# Taller 9 - Interfaz Tkinter sobre el CRUD SQLite (Taller 8)
# ============================================================

NOMBRE_DB = "cibercafe.db"


def crear_tabla():
    conexion = sqlite3.connect(NOMBRE_DB)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            documento TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT,
            membresia TEXT,
            compras REAL
        )
    """)
    conexion.commit()
    conexion.close()


class Cliente:
    def __init__(self, nombre, documento, telefono, membresia="Regular", compras=0):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
        self.membresia = membresia
        self.compras = compras

    def __str__(self):
        return (f"Cliente: {self.nombre} | Documento: {self.documento} | "
                f"Membresía: {self.membresia} | Compras: ${self.compras}")

    # ---------- CREATE ----------
    def guardar(self):
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (documento, nombre, telefono, membresia, compras)
            VALUES (?, ?, ?, ?, ?)
        """, (self.documento, self.nombre, self.telefono, self.membresia, self.compras))
        conexion.commit()
        conexion.close()

    # ---------- READ ----------
    @staticmethod
    def listar_todos():
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("SELECT documento, nombre, telefono, membresia, compras FROM clientes")
        filas = cursor.fetchall()
        conexion.close()
        return filas

    # ---------- UPDATE ----------
    @staticmethod
    def actualizar(documento, nombre, telefono, membresia, compras):
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes SET nombre = ?, telefono = ?, membresia = ?, compras = ?
            WHERE documento = ?
        """, (nombre, telefono, membresia, compras, documento))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas

    # ---------- DELETE ----------
    @staticmethod
    def eliminar(documento):
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE documento = ?", (documento,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas


# ============================================================
# Interfaz gráfica (Tkinter)
# ============================================================

class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Cibercafé - Gestión de Clientes")

        # ---------- Campos Entry (uno por atributo) ----------
        tk.Label(ventana, text="Documento:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_documento = tk.Entry(ventana)
        self.entry_documento.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre = tk.Entry(ventana)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Teléfono:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_telefono = tk.Entry(ventana)
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Membresía:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_membresia = tk.Entry(ventana)
        self.entry_membresia.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(ventana, text="Compras:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.entry_compras = tk.Entry(ventana)
        self.entry_compras.grid(row=4, column=1, padx=5, pady=5)

        # ---------- Botones ----------
        tk.Button(ventana, text="Guardar", width=10, command=self.guardar).grid(row=5, column=0, pady=10)
        tk.Button(ventana, text="Actualizar", width=10, command=self.actualizar).grid(row=5, column=1, pady=10)
        tk.Button(ventana, text="Eliminar", width=10, command=self.eliminar).grid(row=6, column=0, pady=5)
        tk.Button(ventana, text="Limpiar", width=10, command=self.limpiar).grid(row=6, column=1, pady=5)

        # ---------- Listbox ----------
        self.listbox = tk.Listbox(ventana, width=60)
        self.listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_de_lista)

        self.refrescar_lista()

    # ---------- Lógica de la interfaz ----------

    def limpiar(self):
        self.entry_documento.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_membresia.delete(0, tk.END)
        self.entry_compras.delete(0, tk.END)

    def refrescar_lista(self):
        self.listbox.delete(0, tk.END)
        for fila in Cliente.listar_todos():
            documento, nombre, telefono, membresia, compras = fila
            self.listbox.insert(tk.END, f"{documento} | {nombre} | {membresia} | ${compras}")

    def guardar(self):
        if not self.entry_documento.get() or not self.entry_nombre.get():
            messagebox.showwarning("Datos incompletos", "Documento y nombre son obligatorios.")
            return
        try:
            compras = float(self.entry_compras.get() or 0)
        except ValueError:
            messagebox.showwarning("Dato inválido", "Compras debe ser un número.")
            return

        cliente = Cliente(
            nombre=self.entry_nombre.get(),
            documento=self.entry_documento.get(),
            telefono=self.entry_telefono.get(),
            membresia=self.entry_membresia.get() or "Regular",
            compras=compras
        )
        try:
            cliente.guardar()
            messagebox.showinfo("Éxito", f"Cliente {cliente.nombre} guardado.")
            self.limpiar()
            self.refrescar_lista()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un cliente con ese documento.")

    def actualizar(self):
        documento = self.entry_documento.get()
        if not documento:
            messagebox.showwarning("Falta documento", "Selecciona un cliente de la lista o escribe su documento.")
            return
        try:
            compras = float(self.entry_compras.get() or 0)
        except ValueError:
            messagebox.showwarning("Dato inválido", "Compras debe ser un número.")
            return

        filas_afectadas = Cliente.actualizar(
            documento,
            self.entry_nombre.get(),
            self.entry_telefono.get(),
            self.entry_membresia.get() or "Regular",
            compras
        )
        if filas_afectadas:
            messagebox.showinfo("Éxito", "Cliente actualizado.")
            self.limpiar()
            self.refrescar_lista()
        else:
            messagebox.showerror("Error", "No existe un cliente con ese documento.")

    def eliminar(self):
        documento = self.entry_documento.get()
        if not documento:
            messagebox.showwarning("Falta documento", "Selecciona un cliente de la lista o escribe su documento.")
            return

        filas_afectadas = Cliente.eliminar(documento)
        if filas_afectadas:
            messagebox.showinfo("Éxito", "Cliente eliminado.")
            self.limpiar()
            self.refrescar_lista()
        else:
            messagebox.showerror("Error", "No existe un cliente con ese documento.")

    def seleccionar_de_lista(self, evento):
        seleccion = self.listbox.curselection()
        if not seleccion:
            return
        texto = self.listbox.get(seleccion[0])
        documento, nombre, membresia, compras = [p.strip() for p in texto.split("|")]
        compras = compras.replace("$", "")

        # Buscamos el teléfono en la base, ya que no se muestra en el Listbox
        telefono = ""
        for fila in Cliente.listar_todos():
            if fila[0] == documento:
                telefono = fila[2]
                break

        self.limpiar()
        self.entry_documento.insert(0, documento)
        self.entry_nombre.insert(0, nombre)
        self.entry_telefono.insert(0, telefono)
        self.entry_membresia.insert(0, membresia)
        self.entry_compras.insert(0, compras)


if __name__ == "__main__":
    crear_tabla()
    ventana = tk.Tk()
    app = App(ventana)
    ventana.mainloop()