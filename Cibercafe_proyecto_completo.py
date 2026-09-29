# ============================================================
# CIBERCAFÉ - Sistema básico de gestión (POO)
# ============================================================

import sqlite3
import tkinter as tk
from tkinter import messagebox

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
        cursor.execute("""
            INSERT INTO clientes (documento, nombre, telefono, membresia, compras)
            VALUES (?, ?, ?, ?, ?)
        """, (self.documento, self.nombre, self.telefono, self.membresia, self.compras))
        conexion.commit()
        conexion.close()
        print(f"[SQLite] Cliente {self.nombre} guardado en la base de datos.")

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
    def actualizar(documento, nuevas_compras):
        # UPDATE: cambia las compras de un cliente por su documento
        conexion = sqlite3.connect(NOMBRE_DB)
        cursor = conexion.cursor()
        cursor.execute("UPDATE clientes SET compras = ? WHERE documento = ?",
                       (nuevas_compras, documento))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        if filas_afectadas:
            print(f"[SQLite] Cliente {documento} actualizado. Nuevas compras: ${nuevas_compras}")
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


# ============================================================
# Ejemplo de uso
# ============================================================

# 1. Se registra un cliente (datos fijos, una sola vez)
cliente1 = Cliente("Ana Pérez", "1-2345-6789", "8888-1234")
cliente1.registrar_cliente()

# 2. Se crea una computadora del cibercafé
pc1 = Computadora("PC-01", "Windows 11", 500)  # 500 = precio por hora

# 3. Ana llega por primera vez -> se crea una Sesión
sesion1 = Sesion(cliente1, pc1)
sesion1.iniciar_sesion()
sesion1.sumar_tiempo(2)      # usa 2 horas
sesion1.finalizar_sesion()
sesion1.realizar_pago()

print("-" * 40)

# 4. Ana vuelve otro día -> se crea una NUEVA sesión
#    (el cliente es el mismo, pero el tiempo/saldo son independientes)
sesion2 = Sesion(cliente1, pc1)
sesion2.iniciar_sesion()
sesion2.sumar_tiempo(1)      # usa 1 hora esta vez
sesion2.finalizar_sesion()
sesion2.realizar_pago()


# ============================================================
# Taller 3 - Objetos en una lista
# ============================================================

print("=" * 40)

# Clientes y computadoras adicionales para tener sesiones variadas
cliente2 = Cliente("Luis Gómez", "2-3456-7890", "8888-5678")
cliente3 = Cliente("María Rojas", "3-4567-8901", "8888-9012")

pc2 = Computadora("PC-02", "Linux Mint", 400)
pc3 = Computadora("PC-03", "Windows 11", 500)

# 1. Se crean al menos 3 objetos distintos de la clase Sesion
sesion3 = Sesion(cliente1, pc1)   # Ana, nueva sesión (aún sin pagar)
sesion3.sumar_tiempo(2)

sesion4 = Sesion(cliente2, pc2)
sesion4.sumar_tiempo(3)

sesion5 = Sesion(cliente3, pc3)
sesion5.sumar_tiempo(1)

# 2. Se guardan en una lista usando append()
sesiones = []
sesiones.append(sesion3)
sesiones.append(sesion4)
sesiones.append(sesion5)

# 3. Se recorre la lista con un for y se muestra cada objeto
print("=== SESIONES REGISTRADAS ===")
for sesion in sesiones:
    print(sesion.descripcion())


# ============================================================
# Taller 4 - CRUD sobre la lista de Sesiones
# ============================================================

print("=" * 40)

def mostrar_lista(lista):
    # Función de apoyo: recorre e imprime todas las sesiones de la lista
    for sesion in lista:
        print(sesion.descripcion())

# ---------- CREATE (Crear) ----------
# Agregamos al menos 2 objetos nuevos a la lista
cliente4 = Cliente("Pedro Solano", "4-5678-9012", "8888-3456")
pc4 = Computadora("PC-04", "Windows 11", 450)
sesion6 = Sesion(cliente4, pc4)
sesion6.sumar_tiempo(4)
sesiones.append(sesion6)

cliente5 = Cliente("Carla Vindas", "5-6789-0123", "8888-7890")
pc5 = Computadora("PC-05", "Linux Mint", 400)
sesion7 = Sesion(cliente5, pc5)
sesion7.sumar_tiempo(2)
sesiones.append(sesion7)

print("\n--- CREATE: lista después de agregar Pedro y Carla ---")
mostrar_lista(sesiones)

# ---------- READ (Leer) ----------
print("\n--- READ: se recorre y muestra la lista completa ---")
mostrar_lista(sesiones)

# ---------- UPDATE (Actualizar) ----------
# Buscamos una sesión por el número de equipo y le cambiamos un dato
for sesion in sesiones:
    if sesion.computadora.numero_equipo == "PC-02":
        sesion.sumar_tiempo(1)   # se le suma 1 hora más a esa sesión
        break

print("\n--- UPDATE: lista después de sumarle 1 hora a PC-02 ---")
mostrar_lista(sesiones)

# ---------- DELETE (Borrar) ----------
# Eliminamos de la lista la sesión de PC-05
for sesion in sesiones:
    if sesion.computadora.numero_equipo == "PC-05":
        sesiones.remove(sesion)
        break

print("\n--- DELETE: lista después de eliminar la sesión de PC-05 ---")
mostrar_lista(sesiones)


# ============================================================
# Taller 5 - Jerarquía de herencia (Usuario -> Cliente / Empleado)
# ============================================================

print("=" * 40)

# Se crea un objeto de cada subclase
cliente_vip = Cliente("Sofía Araya", "6-7890-1234", "8888-0001", membresia="VIP")
empleado1 = Empleado("Carlos Méndez", "7-8901-2345", "8888-0002", salario=380000)

print("--- Ambos usan saludar(), pero Cliente lo sobreescribió (ver Taller 6) ---")
cliente_vip.saludar()
empleado1.saludar()

print("\n--- Lo que cada uno tiene de PROPIO ---")
cliente_vip.ver_membresia()      # solo Cliente lo tiene
empleado1.cobrar_salario()       # solo Empleado lo tiene


# ============================================================
# Taller 6 - CRUD de Clientes
# ============================================================

print("=" * 40)

def mostrar_clientes(lista):
    # Recorre e imprime cada cliente usando __str__ (print lo llama automáticamente)
    for c in lista:
        print(c)

# ---------- CREATE (Crear) ----------
# Se agregan al menos 2 clientes a la lista
clientes = []
clientes.append(Cliente("Diego Fallas", "8-9012-3456", "8888-1111", membresia="Regular", compras=2000))
clientes.append(Cliente("Valeria Chaves", "9-0123-4567", "8888-2222", membresia="VIP", compras=5000))

print("--- CREATE: clientes agregados ---")
mostrar_clientes(clientes)

# ---------- READ (Leer) ----------
print("\n--- READ: se recorre la lista con __str__ ---")
mostrar_clientes(clientes)

# ---------- UPDATE (Actualizar) ----------
# Se busca un cliente por nombre y se le cambia el dato de compras
for c in clientes:
    if c.nombre == "Diego Fallas":
        c.compras += 1500   # Diego hizo una compra adicional
        break

print("\n--- UPDATE: compras de Diego Fallas actualizadas ---")
mostrar_clientes(clientes)

# ---------- DELETE (Borrar) ----------
# Se elimina un cliente de la lista
for c in clientes:
    if c.nombre == "Valeria Chaves":
        clientes.remove(c)
        break

print("\n--- DELETE: lista después de eliminar a Valeria Chaves ---")
mostrar_clientes(clientes)

# ---------- POLIMORFISMO ----------
# saludar() está sobreescrito en Cliente (ver clase Cliente más arriba).
# Al recorrer una lista de objetos Usuario, cada uno ejecuta SU propia
# versión de saludar() aunque se llame igual en todos.
print("\n--- POLIMORFISMO: mismo método, comportamiento distinto ---")
usuarios_variados = [clientes[0], empleado1]
for u in usuarios_variados:
    u.saludar()


# ============================================================
# Taller 7 - Relaciones entre clases
# ============================================================
# Relaciones del proyecto:
#  - Sesion --> Cliente        : ASOCIACIÓN (el cliente existe sin la sesión)
#  - Sesion --> Computadora    : ASOCIACIÓN (la computadora existe sin la sesión)
#  - Sesion *-- Impresion      : COMPOSICIÓN (la impresión no existe sin la sesión;
#                                la Sesion la crea y la guarda en su lista)

print("=" * 40)

cliente_t7 = Cliente("Elena Mora", "1-1111-2222", "8888-3333")
pc_t7 = Computadora("PC-06", "Windows 11", 500)

sesion_t7 = Sesion(cliente_t7, pc_t7)
sesion_t7.sumar_tiempo(2)            # 2h x $500 = $1000
sesion_t7.solicitar_impresion(10)    # 10 páginas x $50 = $500
sesion_t7.solicitar_impresion(4)     # 4 páginas x $50 = $200

print("\n--- Impresiones de la sesión (composición) ---")
for imp in sesion_t7.impresiones:
    print(f"{imp.paginas} páginas -> ${imp.costo()}")

print(f"\nTotal en impresiones: ${sesion_t7.total_impresiones()}")
print(sesion_t7.descripcion())


# ============================================================
# Taller 8 - CRUD de Cliente con persistencia en SQLite
# ============================================================

print("=" * 40)

crear_tabla()

# CREATE
cliente_db1 = Cliente("Mónica Rojas", "1-9999-0000", "8888-4444", "Regular", 1200)
cliente_db2 = Cliente("Rafael Ureña", "2-8888-1111", "8888-5555", "VIP", 4200)
cliente_db1.guardar()
cliente_db2.guardar()

# READ
print()
Cliente.listar_todos()

# UPDATE
print()
Cliente.actualizar("1-9999-0000", 2000)
print()
Cliente.listar_todos()

# DELETE
print()
Cliente.eliminar("2-8888-1111")
print()
Cliente.listar_todos()


# ============================================================
# Taller 9 - Interfaz Tkinter sobre el CRUD SQLite (Taller 8)
# ============================================================
# Reutiliza guardar(), listar_todos(), actualizar() y eliminar()
# de la clase Cliente, sin duplicar lógica.

class AppClientes:
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

    def limpiar(self):
        self.entry_documento.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_membresia.delete(0, tk.END)
        self.entry_compras.delete(0, tk.END)

    def refrescar_lista(self):
        self.listbox.delete(0, tk.END)
        for documento, nombre, telefono, membresia, compras in Cliente.listar_todos():
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
        # Usa Cliente.actualizar(documento, nuevas_compras) del Taller 8
        documento = self.entry_documento.get()
        if not documento:
            messagebox.showwarning("Falta documento", "Selecciona un cliente de la lista o escribe su documento.")
            return
        try:
            compras = float(self.entry_compras.get() or 0)
        except ValueError:
            messagebox.showwarning("Dato inválido", "Compras debe ser un número.")
            return

        Cliente.actualizar(documento, compras)
        self.limpiar()
        self.refrescar_lista()

    def eliminar(self):
        documento = self.entry_documento.get()
        if not documento:
            messagebox.showwarning("Falta documento", "Selecciona un cliente de la lista o escribe su documento.")
            return

        Cliente.eliminar(documento)
        self.limpiar()
        self.refrescar_lista()

    def seleccionar_de_lista(self, evento):
        seleccion = self.listbox.curselection()
        if not seleccion:
            return
        texto = self.listbox.get(seleccion[0])
        documento, nombre, membresia, compras = [p.strip() for p in texto.split("|")]
        compras = compras.replace("$", "")

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
    print("\nAbriendo interfaz gráfica del Taller 9...")
    ventana = tk.Tk()
    app = AppClientes(ventana)
    ventana.mainloop()