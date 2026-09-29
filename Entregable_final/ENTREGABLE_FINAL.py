# ============================================================
# CIBERCAFÉ - ENTREGABLE FINAL
# Sistema de gestión con POO + SQLite + interfaz Tkinter
# ============================================================
# Los comentarios que empiezan con ">>" explican las partes más
# complejas del código.
#
# Reúne todo lo trabajado en los talleres:
#   Base       -> clases Cliente, Computadora y Sesion
#   Taller 3-4 -> manejo de objetos en listas y CRUD
#   Taller 5   -> herencia: Usuario -> Cliente / Empleado
#   Taller 6   -> polimorfismo (saludar) y __str__
#   Taller 7   -> composición: Sesion *-- Impresion
#   Taller 8   -> persistencia con SQLite (CRUD)
#   Taller 9   -> interfaz gráfica con Tkinter
# ============================================================

import math
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

NOMBRE_DB = "cibercafe.db"
PRECIO_PAGINA = 50            # precio por defecto de cada página impresa
ESTADO_LIBRE = "Disponible"
ESTADO_OCUPADO = "Ocupada"
# >> Se usan constantes en vez de escribir "Ocupada" a mano cada vez:
# >> así, si se comete un error de tipeo, Python lo avisa en lugar de
# >> crear un estado "Ocupda" que nadie notaría.


# ============================================================
# Funciones de apoyo
# ============================================================

def dinero(valor):
    """Formatea un monto: 1200 -> $1,200"""
    valor = float(valor or 0)          # >> "or 0" convierte None en 0
    if valor.is_integer():             # >> 1200.0 -> True, 1200.5 -> False
        return f"${valor:,.0f}"        # >> ",.0f" = separador de miles, sin decimales
    return f"${valor:,.2f}"            # >> si tiene centavos, muestra 2 decimales


def numero(valor):
    """Formatea un número sin ceros de más: 2.0 -> 2 | 1.50 -> 1.5"""
    # >> Paso 1: f"{2.0:.2f}" da "2.00"
    # >> Paso 2: rstrip("0") quita ceros del final -> "2."
    # >> Paso 3: rstrip(".") quita el punto sobrante -> "2"
    texto = f"{float(valor or 0):.2f}".rstrip("0").rstrip(".")
    return texto or "0"                # >> por si el resultado queda vacío


def leer_numero(texto, campo, entero=False, permitir_cero=False):
    """
    Convierte el texto de un Entry a número validando el dato.
    Lanza ValueError con un mensaje claro para mostrar en pantalla.
    """
    # >> strip() quita espacios; replace(",", ".") deja escribir "1,5" o "1.5"
    texto = texto.strip().replace(",", ".")
    try:
        # >> Si entero=True usa int() (rechaza "2.5"); si no, float()
        valor = int(texto) if entero else float(texto)
    except ValueError:
        # >> Se dispara con texto como "abc" o vacío. El mensaje incluye
        # >> el nombre del campo para que el usuario sepa cuál corregir.
        raise ValueError(f"{campo} debe ser un número{' entero' if entero else ''}.")
    # >> float("nan") y float("inf") se convierten sin error, pero no son
    # >> números útiles; isfinite() los detecta y los rechaza.
    if not math.isfinite(valor):
        raise ValueError(f"{campo} no es un número válido.")
    # >> Negativo siempre es inválido. Cero solo es válido si permitir_cero=True
    # >> (por ejemplo, el campo "Compras" puede ser 0, pero las horas no).
    if valor < 0 or (valor == 0 and not permitir_cero):
        if permitir_cero:
            raise ValueError(f"{campo} no puede ser negativo.")
        raise ValueError(f"{campo} debe ser mayor que cero.")
    return valor


def ejecutar(sql, parametros=()):
    """INSERT / UPDATE / DELETE. Devuelve (filas_afectadas, ultimo_id)."""
    conexion = sqlite3.connect(NOMBRE_DB)
    try:
        # >> Los "?" del SQL se reemplazan por 'parametros'. Nunca se
        # >> pegan los datos dentro del texto SQL: así se evita la
        # >> "inyección SQL" (que alguien escriba código SQL en un campo).
        cursor = conexion.execute(sql, parametros)
        conexion.commit()              # >> commit = confirmar y guardar los cambios
        return cursor.rowcount, cursor.lastrowid
    finally:
        # >> finally se ejecuta SIEMPRE, haya error o no: la conexión
        # >> nunca queda abierta.
        conexion.close()


def consultar(sql, parametros=()):
    """SELECT. Devuelve la lista de filas."""
    conexion = sqlite3.connect(NOMBRE_DB)
    try:
        # >> fetchall() devuelve todas las filas como lista de tuplas
        return conexion.execute(sql, parametros).fetchall()
    finally:
        conexion.close()


def crear_tablas():
    # Taller 8 ampliado: además de clientes, ahora se guardan
    # computadoras, sesiones e impresiones.
    conexion = sqlite3.connect(NOMBRE_DB)
    cursor = conexion.cursor()
    # >> "IF NOT EXISTS" hace que este método se pueda ejecutar cada vez
    # >> que se abre el programa sin borrar ni duplicar nada.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            documento TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT,
            membresia TEXT,
            compras REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS computadoras (
            numero_equipo TEXT PRIMARY KEY,
            sistema_operativo TEXT NOT NULL,
            precio_hora REAL NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Disponible'
        )
    """)
    # >> "id INTEGER PRIMARY KEY AUTOINCREMENT": SQLite asigna solo 1, 2, 3...
    # >> "activa" guarda 1 (sesión abierta) o 0 (ya cerrada): SQLite no tiene
    # >> tipo booleano.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento TEXT NOT NULL,
            numero_equipo TEXT NOT NULL,
            tiempo_uso REAL NOT NULL DEFAULT 0,
            saldo_pagar REAL NOT NULL DEFAULT 0,
            total_pagado REAL NOT NULL DEFAULT 0,
            activa INTEGER NOT NULL DEFAULT 1,
            inicio TEXT,
            fin TEXT
        )
    """)
    # >> "sesion_id" enlaza cada impresión con su sesión (relación 1 a muchos:
    # >> una sesión puede tener varias impresiones).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS impresiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id INTEGER NOT NULL,
            paginas INTEGER NOT NULL,
            precio_pagina REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()


# ============================================================
# Clases (POO)
# ============================================================

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
        # >> super().__init__ ejecuta el constructor de Usuario, que guarda
        # >> nombre, documento y teléfono. Así no se repite ese código.
        super().__init__(nombre, documento, telefono)
        self.membresia = membresia   # atributo PROPIO de Cliente
        self.compras = compras       # atributo PROPIO de Cliente (Taller 6)

    def registrar_cliente(self):
        print(f"Cliente {self.nombre} registrado con éxito.")

    def ver_membresia(self):
        print(f"{self.nombre} tiene membresía: {self.membresia}.")

    def saludar(self):
        # POLIMORFISMO (Taller 6): se sobreescribe el saludar() de Usuario
        print(f"Hola, soy {self.nombre}, cliente {self.membresia} del cibercafé.")

    def __str__(self):
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
            # >> Como "documento" es PRIMARY KEY, SQLite rechaza un documento
            # >> repetido con IntegrityError. Aquí se atrapa y solo se imprime.
            # >> Por eso la interfaz (guardar_cliente) revisa ANTES con
            # >> Cliente.obtener(): este error nunca llega hasta la ventana.
            print(f"[SQLite] Ya existe un cliente con documento {self.documento}; no se guardó de nuevo.")
        finally:
            conexion.close()

    @staticmethod
    def listar_todos(imprimir=True):
        # READ: devuelve todos los clientes guardados en SQLite
        # >> @staticmethod: se llama con la clase (Cliente.listar_todos()) sin
        # >> necesitar un objeto Cliente, porque lista TODOS, no uno solo.
        # >> imprimir=False lo usa la interfaz para no llenar la consola.
        filas = consultar("SELECT documento, nombre, telefono, membresia, compras FROM clientes")
        if imprimir:
            print("[SQLite] --- Clientes en la base de datos ---")
            for documento, nombre, telefono, membresia, compras in filas:
                print(f"Cliente: {nombre} | Documento: {documento} | "
                      f"Membresía: {membresia} | Compras: ${compras}")
        return filas

    @staticmethod
    def buscar(texto):
        # READ filtrado (NUEVO): busca por documento o por nombre
        # >> En SQL, LIKE '%ana%' significa "que contenga 'ana' en cualquier
        # >> parte". Los % son comodines. LIKE no distingue mayúsculas.
        patron = f"%{texto}%"
        return consultar("""
            SELECT documento, nombre, telefono, membresia, compras
            FROM clientes
            WHERE documento LIKE ? OR nombre LIKE ?
            ORDER BY nombre
        """, (patron, patron))

    @staticmethod
    def obtener(documento):
        # READ de UN cliente: devuelve un objeto Cliente o None
        filas = consultar("""
            SELECT nombre, telefono, membresia, compras
            FROM clientes WHERE documento = ?
        """, (documento,))
        # >> (documento,) lleva coma para que Python lo trate como tupla de
        # >> un elemento; sin la coma sería solo un texto entre paréntesis.
        if not filas:
            return None
        nombre, telefono, membresia, compras = filas[0]
        # >> Convierte la fila de la BD en un objeto Cliente para poder usar
        # >> sus métodos. "compras or 0" evita valores None.
        return Cliente(nombre, documento, telefono, membresia, compras or 0)

    @staticmethod
    def actualizar(documento, nombre, telefono, membresia, compras):
        # UPDATE: cambia TODOS los datos editables de un cliente por su documento
        filas_afectadas, _ = ejecutar("""
            UPDATE clientes
            SET nombre = ?, telefono = ?, membresia = ?, compras = ?
            WHERE documento = ?
        """, (nombre, telefono, membresia, compras, documento))
        # >> filas_afectadas = 0 significa que ningún cliente tenía ese documento.
        if filas_afectadas:
            print(f"[SQLite] Cliente {documento} actualizado.")
        else:
            print(f"[SQLite] No se encontró un cliente con documento {documento}.")

    @staticmethod
    def sumar_compras(documento, monto):
        # UPDATE puntual (NUEVO): al cobrar una sesión se acumula lo gastado
        # >> "compras = compras + monto" se calcula dentro de SQL. COALESCE
        # >> cambia un valor NULL por 0 (NULL + 100 daría NULL, no 100).
        ejecutar("UPDATE clientes SET compras = COALESCE(compras, 0) + ? WHERE documento = ?",
                 (monto, documento))

    @staticmethod
    def eliminar(documento):
        # DELETE: borra un cliente de la base de datos por su documento
        filas_afectadas, _ = ejecutar("DELETE FROM clientes WHERE documento = ?", (documento,))
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
        super().__init__(nombre, documento, telefono)
        self.salario = salario   # atributo PROPIO de Empleado

    def cobrar_salario(self):
        print(f"{self.nombre} recibió su salario de ${self.salario}.")


class Computadora:
    """
    Representa un equipo físico del cibercafé.
    Ahora también se guarda en SQLite para que el inventario persista.
    """
    def __init__(self, numero_equipo, sistema_operativo, precio_hora, estado=ESTADO_LIBRE):
        self.numero_equipo = numero_equipo
        self.sistema_operativo = sistema_operativo
        self.precio_hora = precio_hora
        self.estado = estado  # Disponible u Ocupada

    def encender(self):
        print(f"Computadora {self.numero_equipo} encendida.")

    def apagar(self):
        print(f"Computadora {self.numero_equipo} apagada.")

    def cambiar_estado(self, nuevo_estado):
        # >> Solo cambia el objeto en memoria. El cambio llega a la base de
        # >> datos cuando la Sesion ejecuta su propio guardar().
        self.estado = nuevo_estado
        print(f"Computadora {self.numero_equipo} ahora está: {self.estado}")

    # ---------- Persistencia SQLite ----------

    def guardar(self):
        # CREATE (lanza sqlite3.IntegrityError si el número ya existe)
        ejecutar("""
            INSERT INTO computadoras (numero_equipo, sistema_operativo, precio_hora, estado)
            VALUES (?, ?, ?, ?)
        """, (self.numero_equipo, self.sistema_operativo, self.precio_hora, self.estado))

    @staticmethod
    def agregar_varias(cantidad, sistema_operativo, precio_hora):
        # Crea 'cantidad' equipos con numeración automática PC-01, PC-02...
        # (usa el primer número libre, así no choca con los que ya existen)
        # >> Se arma un "set" con los nombres existentes: revisar si un nombre
        # >> está en un set es muy rápido.
        existentes = {c.numero_equipo for c in Computadora.listar_todos()}
        creadas = []
        indice = 0
        # >> Bucle: sigue hasta lograr 'cantidad' equipos NUEVOS.
        while len(creadas) < cantidad:
            indice += 1
            # >> f"{indice:02d}" rellena con cero a 2 dígitos: 1 -> "01", 12 -> "12"
            numero_equipo = f"PC-{indice:02d}"
            if numero_equipo in existentes:
                continue   # >> ese nombre ya existe: salta al siguiente número
            Computadora(numero_equipo, sistema_operativo, precio_hora).guardar()
            creadas.append(numero_equipo)
        return creadas
        # >> Ejemplo: si existen PC-01 y PC-03 y se piden 2 equipos, crea PC-02 y PC-04.

    @staticmethod
    def listar_todos():
        # READ: devuelve una lista de objetos Computadora
        # >> ORDER BY length(...), numero_equipo: primero los nombres cortos.
        # >> Sin esto, en orden alfabético "PC-10" saldría antes que "PC-2".
        filas = consultar("""
            SELECT numero_equipo, sistema_operativo, precio_hora, estado
            FROM computadoras
            ORDER BY length(numero_equipo), numero_equipo
        """)
        return [Computadora(n, so, precio, estado) for n, so, precio, estado in filas]

    @staticmethod
    def obtener(numero_equipo):
        filas = consultar("""
            SELECT numero_equipo, sistema_operativo, precio_hora, estado
            FROM computadoras WHERE numero_equipo = ?
        """, (numero_equipo,))
        if not filas:
            return None
        n, so, precio, estado = filas[0]
        return Computadora(n, so, precio, estado)

    @staticmethod
    def eliminar(numero_equipo):
        # DELETE
        ejecutar("DELETE FROM computadoras WHERE numero_equipo = ?", (numero_equipo,))


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
    def __init__(self, cliente, computadora, id_sesion=None):
        # >> La Sesion NO copia los datos del cliente ni del equipo: guarda
        # >> una referencia al objeto completo (asociación, Taller 7).
        self.id = id_sesion            # None hasta que se guarda en SQLite
        self.cliente = cliente
        self.computadora = computadora
        self.tiempo_uso = 0            # horas acumuladas en ESTA sesión
        self.saldo_pagar = 0           # monto pendiente de pago en ESTA sesión
        self.total_pagado = 0          # monto ya cobrado (queda como historial)
        self.impresiones = []          # COMPOSICIÓN (Taller 7)
        self.activa = False
        self.inicio = None
        self.fin = None

    def iniciar_sesion(self, horas_iniciales=0):
        self.computadora.cambiar_estado(ESTADO_OCUPADO)
        self.activa = True
        # >> strftime da formato a la fecha: "2026-09-28 14:30"
        self.inicio = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"{self.cliente.nombre} inició sesión en la computadora {self.computadora.numero_equipo}.")
        if horas_iniciales:
            self.sumar_tiempo(horas_iniciales)
        # >> Al final se guarda: como self.id es None, guardar() hará INSERT
        # >> y así la sesión obtiene su número de id.
        self.guardar()

    def sumar_tiempo(self, horas):
        """
        Acumula horas de uso y calcula el saldo a pagar según el
        precio de la computadora. También se usa para el TIEMPO EXTRA.
        """
        self.tiempo_uso += horas
        # >> Costo de estas horas = horas x precio por hora del equipo.
        # >> Se SUMA al saldo, así que las horas extra no borran lo anterior.
        self.saldo_pagar += horas * self.computadora.precio_hora
        print(f"Se sumaron {horas} horas. Tiempo total: {self.tiempo_uso}h. "
              f"Saldo a pagar: ${self.saldo_pagar}")

    def finalizar_sesion(self):
        self.computadora.cambiar_estado(ESTADO_LIBRE)
        self.activa = False
        self.fin = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"Sesión de {self.cliente.nombre} finalizada. "
              f"Total a pagar: ${self.saldo_pagar}")

    def realizar_pago(self):
        print(f"{self.cliente.nombre} pagó ${self.saldo_pagar}.")
        # >> Antes de poner el saldo en 0, se guarda en total_pagado para no
        # >> perder cuánto se cobró (queda como historial en la BD).
        self.total_pagado += self.saldo_pagar
        self.saldo_pagar = 0

    def solicitar_impresion(self, paginas, precio_pagina=PRECIO_PAGINA):
        """
        Taller 7: la Sesion CREA su propia Impresion (composición),
        la guarda en su lista y suma el costo al saldo a pagar.
        """
        # >> COMPOSICIÓN: la Impresion se crea AQUÍ, dentro de la Sesion, y
        # >> solo existe dentro de su lista. Nadie más la crea desde afuera.
        impresion = Impresion(paginas, precio_pagina)
        self.impresiones.append(impresion)
        self.saldo_pagar += impresion.costo()
        print(f"Impresión de {paginas} páginas agregada. Saldo a pagar: ${self.saldo_pagar}")

    def total_impresiones(self):
        # >> Expresión generadora: suma el costo() de cada impresión de la lista.
        return sum(i.costo() for i in self.impresiones)

    def total_paginas(self):
        return sum(i.paginas for i in self.impresiones)

    def descripcion(self):
        return (f"Cliente: {self.cliente.nombre} | "
                f"Equipo: {self.computadora.numero_equipo} | "
                f"Tiempo: {self.tiempo_uso}h | "
                f"Saldo: ${self.saldo_pagar}")

    # ---------- Persistencia SQLite ----------

    def guardar(self):
        """
        Inserta la sesión (si es nueva) o la actualiza, guarda sus
        impresiones y sincroniza el estado de la computadora.
        Todo en una sola transacción: o se guarda todo o nada.
        """
        # >> Aquí NO se usa ejecutar() porque hacemos VARIAS operaciones que
        # >> deben tratarse como una sola unidad. Una sola conexión y un solo
        # >> commit() al final = transacción: si algo falla a mitad de camino,
        # >> no se guarda nada y la base queda consistente.
        conexion = sqlite3.connect(NOMBRE_DB)
        try:
            cursor = conexion.cursor()
            if self.id is None:
                # >> Sesión NUEVA (todavía sin id): INSERT
                cursor.execute("""
                    INSERT INTO sesiones
                        (documento, numero_equipo, tiempo_uso, saldo_pagar,
                         total_pagado, activa, inicio, fin)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (self.cliente.documento, self.computadora.numero_equipo,
                      self.tiempo_uso, self.saldo_pagar, self.total_pagado,
                      int(self.activa), self.inicio, self.fin))
                # >> lastrowid = el id que SQLite acaba de asignar. Se guarda
                # >> en el objeto para que la próxima vez sea un UPDATE.
                self.id = cursor.lastrowid
            else:
                # >> Sesión que YA existe: UPDATE. Solo cambian estos campos
                # >> (cliente, equipo e inicio no cambian nunca).
                cursor.execute("""
                    UPDATE sesiones
                    SET tiempo_uso = ?, saldo_pagar = ?, total_pagado = ?,
                        activa = ?, fin = ?
                    WHERE id = ?
                """, (self.tiempo_uso, self.saldo_pagar, self.total_pagado,
                      int(self.activa), self.fin, self.id))
            # >> Impresiones: en vez de calcular cuáles son nuevas, se BORRAN
            # >> todas las de esta sesión y se vuelven a insertar desde la
            # >> lista en memoria. Es más simple y seguro para pocos datos.
            cursor.execute("DELETE FROM impresiones WHERE sesion_id = ?", (self.id,))
            # >> executemany repite el INSERT una vez por cada tupla de la lista.
            cursor.executemany(
                "INSERT INTO impresiones (sesion_id, paginas, precio_pagina) VALUES (?, ?, ?)",
                [(self.id, i.paginas, i.precio_pagina) for i in self.impresiones])
            # >> Sincroniza el estado del equipo (Ocupada / Disponible) en la
            # >> misma transacción: sesión y equipo nunca quedan contradictorios.
            cursor.execute("UPDATE computadoras SET estado = ? WHERE numero_equipo = ?",
                           (self.computadora.estado, self.computadora.numero_equipo))
            conexion.commit()   # >> recién aquí se confirma TODO junto
        finally:
            conexion.close()

    @staticmethod
    def listar_activas():
        # READ: reconstruye como objetos las sesiones que siguen abiertas
        # >> Al cerrar y reabrir el programa, en memoria no queda nada; este
        # >> método vuelve a armar los objetos Sesion desde la base de datos.
        filas = consultar("""
            SELECT id, documento, numero_equipo, tiempo_uso, saldo_pagar,
                   total_pagado, inicio
            FROM sesiones WHERE activa = 1 ORDER BY id
        """)
        sesiones = []
        for id_sesion, documento, numero_equipo, tiempo, saldo, pagado, inicio in filas:
            # >> Cada fila solo trae el documento y el número de equipo (texto).
            # >> Se buscan los objetos completos para armar la Sesion.
            cliente = Cliente.obtener(documento)
            equipo = Computadora.obtener(numero_equipo)
            if cliente is None or equipo is None:
                continue   # >> si el cliente o el equipo fue borrado, se omite
            sesion = Sesion(cliente, equipo, id_sesion)
            # >> Se restauran los valores guardados (el constructor los pone en 0).
            sesion.activa = True
            sesion.tiempo_uso = tiempo
            sesion.saldo_pagar = saldo
            sesion.total_pagado = pagado
            sesion.inicio = inicio
            # >> Se recargan las impresiones de esta sesión (composición):
            # >> cada fila de la tabla se convierte otra vez en un objeto Impresion.
            impresiones = consultar(
                "SELECT paginas, precio_pagina FROM impresiones WHERE sesion_id = ? ORDER BY id",
                (id_sesion,))
            for paginas, precio in impresiones:
                sesion.impresiones.append(Impresion(paginas, precio))
            sesiones.append(sesion)
        return sesiones

    @staticmethod
    def cliente_tiene_sesion_activa(documento):
        # >> COUNT(*) devuelve una sola fila con una sola columna: el conteo.
        # >> filas[0][0] = primera fila, primera columna.
        filas = consultar("SELECT COUNT(*) FROM sesiones WHERE documento = ? AND activa = 1",
                          (documento,))
        return filas[0][0] > 0


# ============================================================
# Interfaz gráfica (Taller 9 ampliado)
# ============================================================

def crear_treeview(padre, columnas, altura=10):
    """
    Crea una tabla (Treeview) con barra de desplazamiento.
    columnas: lista de (id, encabezado, ancho, alineación).
    Devuelve (contenedor, tabla).
    """
    # >> Un Frame agrupa la tabla y su barra para poder ubicarlos juntos.
    contenedor = ttk.Frame(padre)
    # >> show="headings" oculta la columna vacía de árbol y muestra solo
    # >> encabezados. selectmode="browse" permite seleccionar UNA fila a la vez.
    tabla = ttk.Treeview(contenedor, columns=[c[0] for c in columnas],
                         show="headings", height=altura, selectmode="browse")
    for id_columna, texto, ancho, ancla in columnas:
        tabla.heading(id_columna, text=texto)
        tabla.column(id_columna, width=ancho, anchor=ancla)   # anchor: w=izq, e=der, center
    # >> La barra y la tabla se conectan en las dos direcciones: mover la
    # >> barra desplaza la tabla (command) y desplazar la tabla mueve la barra.
    barra = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return contenedor, tabla


class AppCibercafe:
    def __init__(self, ventana):
        self.ventana = ventana
        self.sesiones_activas = {}   # iid (id de sesión como texto) -> objeto Sesion
        self.mapa_clientes = {}      # texto del combobox -> documento
        # >> Los dos diccionarios sirven de "puente" entre lo que se ve en
        # >> pantalla (texto) y los objetos reales del programa.

        ventana.title("Cibercafé - Sistema de gestión")
        ventana.geometry("980x660")
        ventana.minsize(900, 600)

        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")   # >> tema más moderno que el de defecto
        except tk.TclError:
            pass                       # >> si el tema no existe, sigue con el de defecto
        estilo.configure("Treeview", rowheight=26, font=("Arial", 10))
        estilo.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        estilo.configure("TNotebook.Tab", padding=(18, 8), font=("Arial", 10, "bold"))
        estilo.configure("Accion.TButton", font=("Arial", 10, "bold"), padding=6)

        # Barra de estado (se empaqueta primero para que siempre quede visible)
        # >> pack() reparte el espacio en el ORDEN en que se llama. Si la barra
        # >> se empaquetara después del notebook (que se expande), podría
        # >> quedar cortada al achicar la ventana.
        self.var_resumen = tk.StringVar()
        ttk.Label(ventana, textvariable=self.var_resumen, anchor="w",
                  relief="sunken", padding=(8, 5)).pack(side="bottom", fill="x", padx=10, pady=10)

        self.notebook = ttk.Notebook(ventana)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        self._crear_tab_clientes()
        self._crear_tab_equipos()
        self._crear_tab_sesiones()
        self.refrescar_todo()   # >> carga los datos guardados al abrir el programa

    # --------------------------------------------------------
    # Pestaña 1: CLIENTES (crear, buscar, actualizar, eliminar)
    # --------------------------------------------------------
    def _crear_tab_clientes(self):
        # >> El guion bajo inicial (_crear...) indica por convención que el
        # >> método es de uso interno de la clase.
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="  Clientes  ")

        formulario = ttk.LabelFrame(tab, text="Datos del cliente", padding=12)
        formulario.pack(side="left", fill="y", padx=(0, 12))

        # >> Un StringVar por campo, guardados en un diccionario. Un StringVar
        # >> está "enlazado" al Entry: .get() lee lo escrito y .set() lo cambia.
        # >> Así limpiar o llenar el formulario es solo recorrer el diccionario.
        self.var_cli = {campo: tk.StringVar()
                        for campo in ("documento", "nombre", "telefono", "membresia", "compras")}

        # Fila 0-2: Documento, Nombre, Teléfono | Fila 3: Membresía | Fila 4: Compras
        campos_texto = [(0, "Documento:", "documento"), (1, "Nombre:", "nombre"),
                        (2, "Teléfono:", "telefono"), (4, "Compras ($):", "compras")]
        for fila, texto, campo in campos_texto:
            # >> grid(): ubica cada widget en una cuadrícula de filas y columnas.
            # >> sticky="e" alinea la etiqueta a la derecha, junto a su campo.
            ttk.Label(formulario, text=texto).grid(row=fila, column=0, sticky="e", padx=5, pady=6)
            ttk.Entry(formulario, textvariable=self.var_cli[campo], width=24).grid(
                row=fila, column=1, padx=5, pady=6)

        ttk.Label(formulario, text="Membresía:").grid(row=3, column=0, sticky="e", padx=5, pady=6)
        # >> state="readonly": solo se puede elegir de la lista, no escribir
        # >> (así nunca queda una membresía inventada).
        ttk.Combobox(formulario, textvariable=self.var_cli["membresia"],
                     values=("Regular", "VIP"), state="readonly", width=21).grid(
            row=3, column=1, padx=5, pady=6)

        botones = ttk.Frame(formulario)
        botones.grid(row=5, column=0, columnspan=2, pady=(12, 0))
        # >> command=self.guardar_cliente SIN paréntesis: se pasa el método
        # >> para que se ejecute al hacer clic. Con paréntesis se ejecutaría
        # >> inmediatamente al crear el botón.
        ttk.Button(botones, text="Guardar nuevo", width=14,
                   command=self.guardar_cliente).grid(row=0, column=0, padx=4, pady=4)
        ttk.Button(botones, text="Actualizar", width=14,
                   command=self.actualizar_cliente).grid(row=0, column=1, padx=4, pady=4)
        ttk.Button(botones, text="Eliminar", width=14,
                   command=self.eliminar_cliente).grid(row=1, column=0, padx=4, pady=4)
        ttk.Button(botones, text="Limpiar", width=14,
                   command=self.limpiar_cliente).grid(row=1, column=1, padx=4, pady=4)

        derecha = ttk.Frame(tab)
        derecha.pack(side="left", fill="both", expand=True)

        buscador = ttk.Frame(derecha)
        buscador.pack(fill="x", pady=(0, 8))
        ttk.Label(buscador, text="Buscar por documento o nombre:").pack(side="left")
        self.var_busqueda = tk.StringVar()
        # >> trace_add("write", ...): ejecuta la función CADA VEZ que cambia el
        # >> texto del buscador. Por eso la lista se filtra mientras se escribe,
        # >> sin botón "Buscar". El lambda ignora los argumentos (*_) que Tk envía.
        self.var_busqueda.trace_add("write", lambda *_: self.refrescar_clientes())
        ttk.Entry(buscador, textvariable=self.var_busqueda).pack(side="left", fill="x",
                                                                 expand=True, padx=8)
        ttk.Button(buscador, text="Ver todos",
                   command=lambda: self.var_busqueda.set("")).pack(side="left")

        contenedor, self.tabla_clientes = crear_treeview(derecha, [
            ("documento", "Documento", 110, "w"),
            ("nombre", "Nombre", 190, "w"),
            ("telefono", "Teléfono", 100, "w"),
            ("membresia", "Membresía", 90, "center"),
            ("compras", "Compras", 90, "e"),
        ], altura=15)
        contenedor.pack(fill="both", expand=True)
        # >> bind: cuando se selecciona una fila, se ejecuta seleccionar_cliente,
        # >> que llena el formulario con los datos de ese cliente.
        self.tabla_clientes.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

        self.limpiar_cliente()   # >> deja el formulario con sus valores por defecto

    def limpiar_cliente(self):
        for campo, variable in self.var_cli.items():
            variable.set("")
        self.var_cli["membresia"].set("Regular")
        self.var_cli["compras"].set("0")
        seleccion = self.tabla_clientes.selection()
        if seleccion:
            self.tabla_clientes.selection_remove(seleccion)   # >> quita el resaltado de la fila

    def refrescar_clientes(self):
        texto = self.var_busqueda.get().strip()
        # >> Si hay texto en el buscador, filtra; si no, muestra todos.
        filas = Cliente.buscar(texto) if texto else Cliente.listar_todos(imprimir=False)
        # >> Se vacía la tabla y se vuelve a llenar. delete(*lista) recibe cada
        # >> elemento de la lista como argumento aparte (el * "desempaqueta").
        self.tabla_clientes.delete(*self.tabla_clientes.get_children())
        for documento, nombre, telefono, membresia, compras in filas:
            # >> iid=documento: el identificador interno de la fila ES el
            # >> documento. Así, al seleccionar una fila se sabe de qué cliente
            # >> se trata sin depender del texto que se ve en pantalla.
            self.tabla_clientes.insert("", "end", iid=documento,
                                       values=(documento, nombre, telefono, membresia, dinero(compras)))

    def seleccionar_cliente(self, _evento=None):
        seleccion = self.tabla_clientes.selection()
        if not seleccion:
            return
        # >> seleccion[0] es el iid = documento. Se consulta el cliente a la BD
        # >> en lugar de leer el texto de la tabla: los valores mostrados
        # >> están formateados ("$1,200") y podrían perder datos (ej. ceros
        # >> iniciales de un documento).
        cliente = Cliente.obtener(seleccion[0])
        if cliente is None:
            return
        self.var_cli["documento"].set(cliente.documento)
        self.var_cli["nombre"].set(cliente.nombre)
        self.var_cli["telefono"].set(cliente.telefono or "")
        self.var_cli["membresia"].set(cliente.membresia or "Regular")
        self.var_cli["compras"].set(numero(cliente.compras))

    def _leer_formulario_cliente(self):
        """Devuelve un Cliente con los datos del formulario o None si hay errores."""
        # >> Método auxiliar compartido por guardar_cliente y actualizar_cliente:
        # >> las dos validan exactamente lo mismo, así no se repite el código.
        documento = self.var_cli["documento"].get().strip()
        nombre = self.var_cli["nombre"].get().strip()
        if not documento or not nombre:
            messagebox.showwarning("Datos incompletos", "Documento y nombre son obligatorios.")
            return None
        try:
            compras = leer_numero(self.var_cli["compras"].get() or "0", "Compras",
                                  permitir_cero=True)
        except ValueError as error:
            # >> str(error) es el mensaje que escribió leer_numero
            messagebox.showwarning("Dato inválido", str(error))
            return None
        return Cliente(nombre, documento, self.var_cli["telefono"].get().strip(),
                       self.var_cli["membresia"].get() or "Regular", compras)

    def guardar_cliente(self):
        cliente = self._leer_formulario_cliente()
        if cliente is None:
            return
        # >> Se revisa ANTES de guardar si el documento ya existe (ver la
        # >> explicación en Cliente.guardar sobre el IntegrityError).
        if Cliente.obtener(cliente.documento):
            messagebox.showerror("Cliente repetido",
                                 "Ya existe un cliente con ese documento.\n"
                                 "Usa «Actualizar» si quieres modificarlo.")
            return
        cliente.guardar()
        messagebox.showinfo("Éxito", f"Cliente {cliente.nombre} guardado.")
        self.limpiar_cliente()
        self.refrescar_todo()

    def actualizar_cliente(self):
        cliente = self._leer_formulario_cliente()
        if cliente is None:
            return
        if Cliente.obtener(cliente.documento) is None:
            messagebox.showwarning("Cliente no encontrado",
                                   "No existe un cliente con ese documento.\n"
                                   "Selecciónalo de la lista o usa «Guardar nuevo».")
            return
        Cliente.actualizar(cliente.documento, cliente.nombre, cliente.telefono,
                           cliente.membresia, cliente.compras)
        messagebox.showinfo("Éxito", f"Cliente {cliente.nombre} actualizado.")
        self.limpiar_cliente()
        self.refrescar_todo()

    def eliminar_cliente(self):
        documento = self.var_cli["documento"].get().strip()
        if not documento:
            messagebox.showwarning("Falta documento",
                                   "Selecciona un cliente de la lista o escribe su documento.")
            return
        cliente = Cliente.obtener(documento)
        if cliente is None:
            messagebox.showwarning("Cliente no encontrado", "No existe un cliente con ese documento.")
            return
        # >> Regla de negocio: no se borra a un cliente que está usando un
        # >> equipo, porque la sesión activa quedaría "huérfana".
        if Sesion.cliente_tiene_sesion_activa(documento):
            messagebox.showwarning("Sesión activa",
                                   f"{cliente.nombre} tiene una sesión activa.\n"
                                   "Finalízala y cóbrala antes de eliminar al cliente.")
            return
        # >> askyesno devuelve True si el usuario pulsa "Sí"
        if not messagebox.askyesno("Confirmar", f"¿Eliminar a {cliente.nombre}?"):
            return
        Cliente.eliminar(documento)
        self.limpiar_cliente()
        self.refrescar_todo()

    # --------------------------------------------------------
    # Pestaña 2: EQUIPOS (agregar computadores y ver su estado)
    # --------------------------------------------------------
    def _crear_tab_equipos(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="  Equipos  ")

        agregar = ttk.LabelFrame(tab, text="Agregar computadores al cibercafé", padding=10)
        agregar.pack(fill="x")

        # >> StringVar con valor inicial: el formulario ya aparece con
        # >> valores razonables (1 equipo, Windows 11, $500).
        self.var_cantidad = tk.StringVar(value="1")
        self.var_so = tk.StringVar(value="Windows 11")
        self.var_precio_equipo = tk.StringVar(value="500")

        ttk.Label(agregar, text="Cantidad:").grid(row=0, column=0, padx=5, pady=4)
        ttk.Spinbox(agregar, from_=1, to=50, width=6,
                    textvariable=self.var_cantidad).grid(row=0, column=1, padx=5)
        ttk.Label(agregar, text="Sistema operativo:").grid(row=0, column=2, padx=(15, 5))
        # >> Este Combobox NO es readonly: se puede elegir de la lista o
        # >> escribir otro sistema operativo.
        ttk.Combobox(agregar, textvariable=self.var_so, width=16,
                     values=("Windows 11", "Windows 10", "Linux Mint", "Ubuntu")).grid(row=0, column=3, padx=5)
        ttk.Label(agregar, text="Precio por hora ($):").grid(row=0, column=4, padx=(15, 5))
        ttk.Entry(agregar, textvariable=self.var_precio_equipo, width=9).grid(row=0, column=5, padx=5)
        ttk.Button(agregar, text="Agregar", style="Accion.TButton",
                   command=self.agregar_equipos).grid(row=0, column=6, padx=(15, 5))

        contenedor, self.tabla_equipos = crear_treeview(tab, [
            ("equipo", "Equipo", 100, "center"),
            ("so", "Sistema operativo", 160, "w"),
            ("precio", "Precio/hora", 100, "e"),
            ("estado", "Estado", 110, "center"),
            ("cliente", "Cliente actual", 220, "w"),
        ], altura=14)
        contenedor.pack(fill="both", expand=True, pady=10)
        # >> tag_configure define "etiquetas" de color. Al insertar una fila con
        # >> tags=("Disponible",) o tags=("Ocupada",) toma el color de su tag.
        # >> (Ver refrescar_equipos.)
        self.tabla_equipos.tag_configure(ESTADO_LIBRE, background="#d4edda", foreground="#155724")
        self.tabla_equipos.tag_configure(ESTADO_OCUPADO, background="#f8d7da", foreground="#721c24")

        acciones = ttk.Frame(tab)
        acciones.pack(fill="x")
        ttk.Button(acciones, text="Ocupar (iniciar sesión)", style="Accion.TButton",
                   command=self.ocupar_equipo).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Liberar (finalizar y cobrar)", style="Accion.TButton",
                   command=self.liberar_equipo).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Eliminar equipo",
                   command=self.eliminar_equipo).pack(side="right")

    def refrescar_equipos(self):
        # >> Diccionario {equipo: nombre del cliente} construido con las
        # >> sesiones activas. Sirve para llenar la columna "Cliente actual".
        # >> Por eso refrescar_todo() carga las sesiones ANTES que los equipos.
        usuario_por_equipo = {s.computadora.numero_equipo: s.cliente.nombre
                              for s in self.sesiones_activas.values()}
        self.tabla_equipos.delete(*self.tabla_equipos.get_children())
        for equipo in Computadora.listar_todos():
            self.tabla_equipos.insert(
                "", "end", iid=equipo.numero_equipo,
                values=(equipo.numero_equipo, equipo.sistema_operativo,
                        dinero(equipo.precio_hora), equipo.estado,
                        # >> .get(clave, "—"): si el equipo no tiene sesión,
                        # >> muestra una raya en lugar de dar error.
                        usuario_por_equipo.get(equipo.numero_equipo, "—")),
                tags=(equipo.estado,))   # >> el estado decide el color de la fila

    def agregar_equipos(self):
        try:
            cantidad = leer_numero(self.var_cantidad.get(), "La cantidad", entero=True)
            precio = leer_numero(self.var_precio_equipo.get(), "El precio por hora")
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            return
        if cantidad > 50:
            messagebox.showwarning("Dato inválido", "Puedes agregar máximo 50 equipos a la vez.")
            return
        sistema = self.var_so.get().strip()
        if not sistema:
            messagebox.showwarning("Datos incompletos", "Indica el sistema operativo.")
            return
        creadas = Computadora.agregar_varias(cantidad, sistema, precio)
        messagebox.showinfo("Equipos agregados",
                            f"Se agregaron {len(creadas)} equipo(s): {', '.join(creadas)}")
        self.refrescar_todo()

    def _equipo_seleccionado(self):
        # >> Auxiliar: devuelve el equipo elegido en la tabla o avisa si no hay
        # >> ninguno. Lo usan ocupar, liberar y eliminar.
        seleccion = self.tabla_equipos.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un equipo", "Primero elige un equipo de la lista.")
            return None
        return Computadora.obtener(seleccion[0])

    def ocupar_equipo(self):
        equipo = self._equipo_seleccionado()
        if equipo is None:
            return
        if equipo.estado == ESTADO_OCUPADO:
            messagebox.showinfo("Equipo ocupado", f"{equipo.numero_equipo} ya tiene una sesión activa.")
            return
        # Lleva al usuario a la pestaña de sesiones con el equipo ya elegido
        # >> Este botón NO cambia el estado directamente: solo prepara el
        # >> formulario de "Nueva sesión". El equipo pasa a Ocupada cuando
        # >> realmente se inicia la sesión (así el estado siempre coincide
        # >> con una sesión real).
        self.combo_equipo.set(equipo.numero_equipo)
        self.notebook.select(2)          # >> la pestaña 2 (empezando en 0) = Sesiones
        self.combo_cliente.focus_set()   # >> deja el cursor listo para elegir cliente

    def liberar_equipo(self):
        equipo = self._equipo_seleccionado()
        if equipo is None:
            return
        if equipo.estado == ESTADO_LIBRE:
            messagebox.showinfo("Equipo disponible", f"{equipo.numero_equipo} ya está libre.")
            return
        # >> Busca, entre las sesiones activas, la que usa este equipo y
        # >> reutiliza el mismo proceso de cobro de la pestaña Sesiones.
        for sesion in self.sesiones_activas.values():
            if sesion.computadora.numero_equipo == equipo.numero_equipo:
                self.cobrar_sesion(sesion)
                return

    def eliminar_equipo(self):
        equipo = self._equipo_seleccionado()
        if equipo is None:
            return
        if equipo.estado == ESTADO_OCUPADO:
            messagebox.showwarning("Equipo ocupado",
                                   f"{equipo.numero_equipo} tiene una sesión activa.\n"
                                   "Finalízala antes de eliminar el equipo.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el equipo {equipo.numero_equipo}?"):
            return
        Computadora.eliminar(equipo.numero_equipo)
        self.refrescar_todo()

    # --------------------------------------------------------
    # Pestaña 3: SESIONES (iniciar, tiempo extra, impresiones, cobrar)
    # --------------------------------------------------------
    def _crear_tab_sesiones(self):
        tab = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(tab, text="  Sesiones  ")

        nueva = ttk.LabelFrame(tab, text="Nueva sesión", padding=10)
        nueva.pack(fill="x")

        ttk.Label(nueva, text="Cliente:").grid(row=0, column=0, padx=5, pady=4)
        # >> Los Combobox se guardan en self.* porque otros métodos necesitan
        # >> leerlos (.get()) o cambiarlos (.set()). Sus opciones se llenan
        # >> en refrescar_combos().
        self.combo_cliente = ttk.Combobox(nueva, state="readonly", width=30)
        self.combo_cliente.grid(row=0, column=1, padx=5)
        ttk.Label(nueva, text="Equipo:").grid(row=0, column=2, padx=(15, 5))
        self.combo_equipo = ttk.Combobox(nueva, state="readonly", width=10)
        self.combo_equipo.grid(row=0, column=3, padx=5)
        ttk.Label(nueva, text="Horas:").grid(row=0, column=4, padx=(15, 5))
        self.var_horas_inicio = tk.StringVar(value="1")
        ttk.Entry(nueva, textvariable=self.var_horas_inicio, width=6).grid(row=0, column=5, padx=5)
        ttk.Button(nueva, text="Iniciar sesión", style="Accion.TButton",
                   command=self.iniciar_sesion).grid(row=0, column=6, padx=(15, 5))

        contenedor, self.tabla_sesiones = crear_treeview(tab, [
            ("id", "N°", 50, "center"),
            ("cliente", "Cliente", 200, "w"),
            ("equipo", "Equipo", 80, "center"),
            ("inicio", "Inicio", 130, "center"),
            ("horas", "Horas", 70, "center"),
            ("paginas", "Págs. impresas", 110, "center"),
            ("saldo", "Saldo a pagar", 110, "e"),
        ], altura=10)
        contenedor.pack(fill="both", expand=True, pady=10)
        self.tabla_sesiones.bind("<<TreeviewSelect>>", self.mostrar_detalle)

        self.var_detalle = tk.StringVar()
        ttk.Label(tab, textvariable=self.var_detalle, font=("Arial", 10, "bold"),
                  anchor="w").pack(fill="x", pady=(0, 8))

        acciones = ttk.LabelFrame(tab, text="Acciones sobre la sesión seleccionada", padding=10)
        acciones.pack(fill="x")

        ttk.Label(acciones, text="Tiempo extra (horas):").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.var_horas_extra = tk.StringVar(value="1")
        ttk.Entry(acciones, textvariable=self.var_horas_extra, width=6).grid(row=0, column=1, padx=5)
        ttk.Button(acciones, text="Agregar tiempo extra",
                   command=self.agregar_tiempo_extra).grid(row=0, column=2, padx=5)

        ttk.Label(acciones, text="Impresión (páginas):").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self.var_paginas = tk.StringVar(value="1")
        ttk.Entry(acciones, textvariable=self.var_paginas, width=6).grid(row=1, column=1, padx=5)
        ttk.Label(acciones, text="Precio por página ($):").grid(row=1, column=3, padx=(15, 5))
        self.var_precio_pagina = tk.StringVar(value=str(PRECIO_PAGINA))
        ttk.Entry(acciones, textvariable=self.var_precio_pagina, width=6).grid(row=1, column=4, padx=5)
        ttk.Button(acciones, text="Agregar impresión",
                   command=self.agregar_impresion).grid(row=1, column=2, padx=5)

        # >> rowspan=2: el botón ocupa dos filas de alto; sticky="ns" lo
        # >> estira de arriba a abajo para que destaque.
        ttk.Button(acciones, text="Finalizar y cobrar", style="Accion.TButton",
                   command=self.finalizar_y_cobrar).grid(row=0, column=5, rowspan=2,
                                                         padx=(40, 5), sticky="ns")

    def refrescar_sesiones(self):
        # >> Se recuerda la fila seleccionada ANTES de vaciar la tabla, para
        # >> poder volver a seleccionarla después (si no, cada acción haría
        # >> perder la selección).
        previa = self.tabla_sesiones.selection()
        # >> Diccionario {id de sesión como texto: objeto Sesion}. Es el "puente"
        # >> entre la fila seleccionada (que solo tiene un iid de texto) y el
        # >> objeto real Sesion con el que se trabaja.
        self.sesiones_activas = {str(s.id): s for s in Sesion.listar_activas()}
        self.tabla_sesiones.delete(*self.tabla_sesiones.get_children())
        for iid, sesion in self.sesiones_activas.items():
            self.tabla_sesiones.insert(
                "", "end", iid=iid,
                values=(sesion.id, sesion.cliente.nombre, sesion.computadora.numero_equipo,
                        sesion.inicio or "", numero(sesion.tiempo_uso),
                        sesion.total_paginas(), dinero(sesion.saldo_pagar)))
        # >> Si la sesión seleccionada antes sigue activa, se vuelve a
        # >> seleccionar. Si ya se cobró, no existe en el diccionario y se omite.
        if previa and previa[0] in self.sesiones_activas:
            self.tabla_sesiones.selection_set(previa[0])
        self.mostrar_detalle()

    def refrescar_combos(self):
        # >> sorted(..., key=lambda f: f[1].lower()): ordena las filas por el
        # >> nombre (posición 1), ignorando mayúsculas.
        clientes = sorted(Cliente.listar_todos(imprimir=False), key=lambda f: f[1].lower())
        # >> "nombre, documento, *_": desempaqueta la fila; el * recoge el
        # >> resto de columnas que aquí no se necesitan.
        # >> El texto del combo incluye el documento para distinguir a dos
        # >> clientes con el mismo nombre.
        self.mapa_clientes = {f"{nombre} ({documento})": documento
                              for documento, nombre, *_ in clientes}
        self.combo_cliente["values"] = list(self.mapa_clientes)
        # >> Si el cliente que estaba elegido ya no existe (fue eliminado),
        # >> se limpia el combo.
        if self.combo_cliente.get() not in self.mapa_clientes:
            self.combo_cliente.set("")

        # >> Solo los equipos DISPONIBLES se ofrecen para iniciar sesión.
        libres = [e.numero_equipo for e in Computadora.listar_todos() if e.estado == ESTADO_LIBRE]
        self.combo_equipo["values"] = libres
        if self.combo_equipo.get() not in libres:
            self.combo_equipo.set("")

    def sesion_seleccionada(self, avisar=True):
        seleccion = self.tabla_sesiones.selection()
        # >> Traduce la fila seleccionada (iid de texto) al objeto Sesion real
        # >> usando el diccionario. Si no hay selección, queda en None.
        sesion = self.sesiones_activas.get(seleccion[0]) if seleccion else None
        # >> avisar=False se usa desde mostrar_detalle, que se ejecuta solo y no
        # >> debe mostrar una ventana emergente cada vez que no hay selección.
        if sesion is None and avisar:
            messagebox.showinfo("Selecciona una sesión", "Primero elige una sesión activa de la lista.")
        return sesion

    def mostrar_detalle(self, _evento=None):
        sesion = self.sesion_seleccionada(avisar=False)
        if sesion is None:
            self.var_detalle.set("Selecciona una sesión para ver su detalle.")
            return
        impresiones = sesion.total_impresiones()
        # >> El saldo incluye tiempo + impresiones, así que el costo del tiempo
        # >> es lo que queda al restar las impresiones.
        tiempo = sesion.saldo_pagar - impresiones
        self.var_detalle.set(
            f"{sesion.cliente.nombre} en {sesion.computadora.numero_equipo}   |   "
            f"Tiempo: {numero(sesion.tiempo_uso)} h = {dinero(tiempo)}   |   "
            f"Impresiones: {sesion.total_paginas()} págs = {dinero(impresiones)}   |   "
            f"TOTAL: {dinero(sesion.saldo_pagar)}")

    def iniciar_sesion(self):
        texto_cliente = self.combo_cliente.get()
        numero_equipo = self.combo_equipo.get()
        # >> El combo devuelve el TEXTO ("Ana Pérez (1-2345)"); mapa_clientes lo
        # >> traduce al documento real. Si el texto no está, no se eligió nada.
        if texto_cliente not in self.mapa_clientes or not numero_equipo:
            messagebox.showwarning("Datos incompletos", "Elige un cliente y un equipo disponible.")
            return
        try:
            horas = leer_numero(self.var_horas_inicio.get(), "Las horas")
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            return
        cliente = Cliente.obtener(self.mapa_clientes[texto_cliente])
        equipo = Computadora.obtener(numero_equipo)
        # >> Se vuelve a consultar el estado en la BD por seguridad: entre que
        # >> se llenó el combo y se pulsó el botón, el equipo pudo cambiar.
        if cliente is None or equipo is None or equipo.estado != ESTADO_LIBRE:
            messagebox.showwarning("No disponible", "Ese equipo ya no está disponible.")
            self.refrescar_todo()
            return
        sesion = Sesion(cliente, equipo)
        # >> iniciar_sesion pone el equipo en Ocupada, suma las horas y guarda
        # >> todo en la BD (ver Sesion.iniciar_sesion y Sesion.guardar).
        sesion.iniciar_sesion(horas)
        self.refrescar_todo()
        # >> Selecciona la sesión recién creada para que se vea su detalle.
        self.tabla_sesiones.selection_set(str(sesion.id))

    def agregar_tiempo_extra(self):
        sesion = self.sesion_seleccionada()
        if sesion is None:
            return
        try:
            horas = leer_numero(self.var_horas_extra.get(), "Las horas extra")
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            return
        # >> Patrón que se repite en casi todos los botones:
        # >> 1) modificar el objeto en memoria, 2) guardarlo en la BD,
        # >> 3) redibujar la pantalla.
        sesion.sumar_tiempo(horas)
        sesion.guardar()
        self.refrescar_todo()

    def agregar_impresion(self):
        sesion = self.sesion_seleccionada()
        if sesion is None:
            return
        try:
            paginas = leer_numero(self.var_paginas.get(), "Las páginas", entero=True)
            precio = leer_numero(self.var_precio_pagina.get(), "El precio por página")
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))
            return
        sesion.solicitar_impresion(paginas, precio)
        sesion.guardar()
        self.refrescar_todo()

    def finalizar_y_cobrar(self):
        sesion = self.sesion_seleccionada()
        if sesion is not None:
            self.cobrar_sesion(sesion)

    def cobrar_sesion(self, sesion):
        # >> Este método lo usan DOS botones: "Finalizar y cobrar" (pestaña
        # >> Sesiones) y "Liberar" (pestaña Equipos).
        # >> El total se guarda en una variable ANTES de cobrar, porque
        # >> realizar_pago() deja el saldo en 0.
        total = sesion.saldo_pagar
        impresiones = sesion.total_impresiones()
        mensaje = (f"Cliente: {sesion.cliente.nombre}\n"
                   f"Equipo: {sesion.computadora.numero_equipo}\n\n"
                   f"Tiempo: {numero(sesion.tiempo_uso)} h  ->  {dinero(total - impresiones)}\n"
                   f"Impresiones: {sesion.total_paginas()} págs  ->  {dinero(impresiones)}\n\n"
                   f"TOTAL A COBRAR: {dinero(total)}\n\n"
                   "¿Confirmar el pago y liberar el equipo?")
        if not messagebox.askyesno("Finalizar y cobrar", mensaje):
            return   # >> si el usuario dice "No", no cambia nada
        # >> Orden importante:
        sesion.finalizar_sesion()   # 1) equipo -> Disponible, sesión inactiva
        sesion.realizar_pago()      # 2) saldo -> total_pagado, saldo en 0
        sesion.guardar()            # 3) se guarda todo en la BD
        Cliente.sumar_compras(sesion.cliente.documento, total)   # 4) suma al cliente
        self.refrescar_todo()

    # --------------------------------------------------------
    # Actualización general de pantalla
    # --------------------------------------------------------
    def refrescar_todo(self):
        # >> El ORDEN importa: las sesiones van primero porque refrescar_equipos
        # >> las necesita para mostrar el nombre del cliente de cada equipo.
        self.refrescar_sesiones()   # primero: los demás dependen de las sesiones activas
        self.refrescar_equipos()
        self.refrescar_clientes()
        self.refrescar_combos()
        self.actualizar_resumen()

    def actualizar_resumen(self):
        equipos = Computadora.listar_todos()
        # >> sum(1 for ...) cuenta cuántos equipos cumplen la condición.
        ocupados = sum(1 for e in equipos if e.estado == ESTADO_OCUPADO)
        self.var_resumen.set(
            f"Equipos: {len(equipos)}     |     Disponibles: {len(equipos) - ocupados}"
            f"     |     Ocupados: {ocupados}     |     Sesiones activas: {len(self.sesiones_activas)}")


def main():
    crear_tablas()          # >> primero la BD (se crea sola la primera vez)
    ventana = tk.Tk()       # >> la ventana principal
    AppCibercafe(ventana)   # >> se construye toda la interfaz
    ventana.mainloop()      # >> queda esperando clics y teclas hasta cerrar la ventana


# >> Esta condición es True solo si se ejecuta el archivo directamente
# >> (python ENTREGABLE_FINAL.py) y False si otro archivo lo importa.
if __name__ == "__main__":
    main()