# ============================================================
# CIBERCAFÉ - Sistema básico de gestión (POO)
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