# ============================================================
# CIBERCAFÉ - Capa de lógica y datos (sin interfaz gráfica)
# Clases (POO) + acceso a SQLite. Es lo que empaqueta el Dockerfile.
# ============================================================

import sqlite3

NOMBRE_DB = "cibercafe.db"


def crear_tabla():
    # Taller 8: crea la tabla de clientes en SQLite si no existe
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


class Usuario:
    """
    Clase BASE (Taller 5): agrupa lo que TODA persona relacionada
    al cibercafé tiene en común, sin importar si es cliente o empleado.
    """
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def saludar(self):
        print(f"Hola, soy {self.nombre} (documento: {self.documento}).")


class Cliente(Usuario):
    """
    Subclase de Usuario. Guarda datos FIJOS del cliente
    (no cambian según la visita) más su propio atributo/método.
    """
    def __init__(self, nombre, documento, telefono, membresia="Regular", compras=0):
        # Reutiliza el constructor de Usuario en vez de repetir código
        super().__init__(nombre, documento, telefono)
        self.membresia = membresia   # atributo PROPIO de Cliente
        self.compras = compras       # atributo PROPIO de Cliente (Taller 6)

    def registrar_cliente(self):
        print(f"Cliente {self.nombre} registrado con éxito.")

    def ver_membresia(self):
        # método PROPIO de Cliente
        print(f"{self.nombre} tiene membresía: {self.membresia}.")

    def saludar(self):
        # POLIMORFISMO (Taller 6): se sobreescribe el saludar() de Usuario
        # para que un Cliente salude mencionando también su membresía.
        print(f"Hola, soy {self.nombre}, cliente {self.membresia} del cibercafé.")

    def __str__(self):
        # Se usa en el Taller 6 para mostrar el cliente con print()
        return (f"Cliente: {self.nombre} | Documento: {self.documento} | "
                f"Membresía: {self.membresia} | Compras: ${self.compras}")

    # ---------- Persistencia SQLite (Taller 8) ----------

    def guardar(self):
        # CREATE: inserta este cliente en la base de datos
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO clientes (documento, nombre, telefono, membresia, compras)
                VALUES (?, ?, ?, ?, ?)
            """, (self.documento, self.nombre, self.telefono, self.membresia, self.compras))
            conexion.commit()
            print(f"[SQLite] Cliente {self.nombre} guardado en la base de datos.")
        except sqlite3.IntegrityError:
            print(f"[SQLite] Ya existe un cliente con documento {self.documento}; no se guardó de nuevo.")
        finally:
            conexion.close()

    @staticmethod
    def listar_todos():
        # READ: devuelve todos los clientes guardados en SQLite
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("SELECT documento, nombre, telefono, membresia, compras FROM clientes")
        filas = cursor.fetchall()
        conexion.close()

        print("[SQLite] --- Clientes en la base de datos ---")
        for documento, nombre, telefono, membresia, compras in filas:
            print(f"Cliente: {nombre} | Documento: {documento} | "
                  f"Membresía: {membresia} | Compras: ${compras}")
        return filas

    @staticmethod
    def actualizar(documento, nombre, telefono, membresia, compras):
        # UPDATE: cambia TODOS los datos editables de un cliente por su documento
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, telefono = ?, membresia = ?, compras = ?
            WHERE documento = ?
        """, (nombre, telefono, membresia, compras, documento))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        if filas_afectadas:
            print(f"[SQLite] Cliente {documento} actualizado.")
        else:
            print(f"[SQLite] No se encontró un cliente con documento {documento}.")

    @staticmethod
    def eliminar(documento):
        # DELETE: borra un cliente de la base de datos por su documento
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE documento = ?", (documento,))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        if filas_afectadas:
            print(f"[SQLite] Cliente {documento} eliminado de la base de datos.")
        else:
            print(f"[SQLite] No se encontró un cliente con documento {documento}.")


class Empleado(Usuario):
    """
    Subclase de Usuario (Taller 5). Representa al personal
    que trabaja en el cibercafé.
    """
    def __init__(self, nombre, documento, telefono, salario):
        # Reutiliza el constructor de Usuario en vez de repetir código
        super().__init__(nombre, documento, telefono)
        self.salario = salario   # atributo PROPIO de Empleado

    def cobrar_salario(self):
        # método PROPIO de Empleado
        print(f"{self.nombre} recibió su salario de ${self.salario}.")


class Computadora:
    """
    Representa un equipo físico del cibercafé.
    """
    def __init__(self, numero_equipo, sistema_operativo, precio_hora):
        self.numero_equipo = numero_equipo
        self.sistema_operativo = sistema_operativo
        self.precio_hora = precio_hora
        self.estado = "Disponible"  # Disponible u Ocupada

    def encender(self):
        print(f"Computadora {self.numero_equipo} encendida.")

    def apagar(self):
        print(f"Computadora {self.numero_equipo} apagada.")

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        print(f"Computadora {self.numero_equipo} ahora está: {self.estado}")


class Impresion:
    """
    Trabajo de impresión (Taller 7). Es la PARTE de una Sesion:
    no existe por sí sola, siempre se crea dentro de una sesión.
    """
    def __init__(self, paginas, precio_pagina):
        self.paginas = paginas
        self.precio_pagina = precio_pagina

    def costo(self):
        return self.paginas * self.precio_pagina


class Sesion:
    """
    Representa UNA visita/uso del cibercafé por parte de un cliente
    en una computadora específica. Aquí sí viven tiempo_uso y saldo_pagar,
    porque cambian cada vez que el cliente usa el servicio.
    """
    def __init__(self, cliente, computadora):
        self.cliente = cliente
        self.computadora = computadora
        self.tiempo_uso = 0        # horas acumuladas en ESTA sesión
        self.saldo_pagar = 0       # monto a pagar en ESTA sesión
        self.impresiones = []      # COMPOSICIÓN (Taller 7): las impresiones viven dentro de la sesión

    def iniciar_sesion(self):
        self.computadora.cambiar_estado("Ocupada")
        print(f"{self.cliente.nombre} inició sesión en la computadora {self.computadora.numero_equipo}.")

    def sumar_tiempo(self, horas):
        """
        Método que SÍ hace algo: acumula horas de uso
        y calcula el saldo a pagar según el precio de la computadora.
        """
        self.tiempo_uso += horas
        self.saldo_pagar += horas * self.computadora.precio_hora
        print(f"Se sumaron {horas} horas. Tiempo total: {self.tiempo_uso}h. "
              f"Saldo a pagar: ${self.saldo_pagar}")

    def finalizar_sesion(self):
        self.computadora.cambiar_estado("Disponible")
        print(f"Sesión de {self.cliente.nombre} finalizada. "
              f"Total a pagar: ${self.saldo_pagar}")

    def realizar_pago(self):
        print(f"{self.cliente.nombre} pagó ${self.saldo_pagar}.")
        self.saldo_pagar = 0

    def solicitar_impresion(self, paginas, precio_pagina=50):
        """
        Taller 7: la Sesion CREA su propia Impresion (composición),
        la guarda en su lista y suma el costo al saldo a pagar.
        """
        impresion = Impresion(paginas, precio_pagina)
        self.impresiones.append(impresion)
        self.saldo_pagar += impresion.costo()
        print(f"Impresión de {paginas} páginas agregada. Saldo a pagar: ${self.saldo_pagar}")

    def total_impresiones(self):
        return sum(i.costo() for i in self.impresiones)

    def descripcion(self):
        # Método usado en el Taller 3 para mostrar la sesión dentro de una lista
        return (f"Cliente: {self.cliente.nombre} | "
                f"Equipo: {self.computadora.numero_equipo} | "
                f"Tiempo: {self.tiempo_uso}h | "
                f"Saldo: ${self.saldo_pagar}")
