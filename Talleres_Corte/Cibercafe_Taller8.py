import sqlite3

# ============================================================
# Taller 8 - CRUD de Cliente en SQLite
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
        print(f"Cliente {self.nombre} guardado en la base de datos.")

    # ---------- READ ----------
    @staticmethod
    def listar_todos():
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("SELECT documento, nombre, telefono, membresia, compras FROM clientes")
        filas = cursor.fetchall()
        conexion.close()

        print("--- Clientes en la base de datos ---")
        for fila in filas:
            documento, nombre, telefono, membresia, compras = fila
            print(f"Cliente: {nombre} | Documento: {documento} | "
                  f"Membresía: {membresia} | Compras: ${compras}")
        return filas

    # ---------- UPDATE ----------
    @staticmethod
    def actualizar(documento, nuevas_compras):
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes SET compras = ? WHERE documento = ?
        """, (nuevas_compras, documento))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        if filas_afectadas:
            print(f"Cliente {documento} actualizado. Nuevas compras: ${nuevas_compras}")
        else:
            print(f"No se encontró un cliente con documento {documento}.")

    # ---------- DELETE ----------
    @staticmethod
    def eliminar(documento):
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE documento = ?", (documento,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        if filas_afectadas:
            print(f"Cliente {documento} eliminado de la base de datos.")
        else:
            print(f"No se encontró un cliente con documento {documento}.")


# ============================================================
# Prueba de las 4 operaciones
# ============================================================

crear_tabla()

# CREATE
cliente1 = Cliente("Diego Fallas", "8-9012-3456", "8888-1111", "Regular", 2000)
cliente2 = Cliente("Valeria Chaves", "9-0123-4567", "8888-2222", "VIP", 5000)
cliente1.guardar()
cliente2.guardar()

# READ
print()
Cliente.listar_todos()

# UPDATE
print()
Cliente.actualizar("8-9012-3456", 3500)
print()
Cliente.listar_todos()

# DELETE
print()
Cliente.eliminar("9-0123-4567")
print()
Cliente.listar_todos()