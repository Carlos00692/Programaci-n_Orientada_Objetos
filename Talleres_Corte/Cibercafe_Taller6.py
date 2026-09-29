class Usuario:
    """
    Clase base con lo común a cualquier persona del cibercafé.
    """
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def saludar(self):
        print(f"Hola, soy {self.nombre} (documento: {self.documento}).")


class Cliente(Usuario):
    def __init__(self, nombre, documento, telefono, membresia="Regular", compras=0):
        super().__init__(nombre, documento, telefono)
        self.membresia = membresia
        self.compras = compras

    def saludar(self):
        # POLIMORFISMO: se sobreescribe el saludar() de Usuario
        print(f"Hola, soy {self.nombre}, cliente {self.membresia} del cibercafé.")

    def __str__(self):
        # Se usa para mostrar el cliente directamente con print()
        return (f"Cliente: {self.nombre} | Documento: {self.documento} | "
                f"Membresía: {self.membresia} | Compras: ${self.compras}")


class Empleado(Usuario):
    """
    Se incluye solo para poder demostrar el polimorfismo:
    usa el saludar() ORIGINAL de Usuario, sin sobreescribirlo.
    """
    def __init__(self, nombre, documento, telefono, salario):
        super().__init__(nombre, documento, telefono)
        self.salario = salario


def mostrar_clientes(lista):
    # Recorre e imprime cada cliente usando __str__ (print lo llama automáticamente)
    for c in lista:
        print(c)


# ============================================================
# Taller 6 - CRUD de Clientes
# ============================================================

# ---------- CREATE (Crear) ----------
clientes = []
clientes.append(Cliente("Diego Fallas", "8-9012-3456", "8888-1111", membresia="Regular", compras=2000))
clientes.append(Cliente("Valeria Chaves", "9-0123-4567", "8888-2222", membresia="VIP", compras=5000))

print("--- CREATE: clientes agregados ---")
mostrar_clientes(clientes)

# ---------- READ (Leer) ----------
print("\n--- READ: se recorre la lista con __str__ ---")
mostrar_clientes(clientes)

# ---------- UPDATE (Actualizar) ----------
for c in clientes:
    if c.nombre == "Diego Fallas":
        c.compras += 1500   # Diego hizo una compra adicional
        break

print("\n--- UPDATE: compras de Diego Fallas actualizadas ---")
mostrar_clientes(clientes)

# ---------- DELETE (Borrar) ----------
for c in clientes:
    if c.nombre == "Valeria Chaves":
        clientes.remove(c)
        break

print("\n--- DELETE: lista después de eliminar a Valeria Chaves ---")
mostrar_clientes(clientes)

# ---------- POLIMORFISMO ----------
# saludar() está sobreescrito en Cliente. Al recorrer una lista de
# objetos Usuario, cada uno ejecuta SU PROPIA versión del método,
# aunque se llame igual en todos.
empleado1 = Empleado("Carlos Méndez", "7-8901-2345", "8888-0002", salario=380000)

print("\n--- POLIMORFISMO: mismo método, comportamiento distinto ---")
usuarios_variados = [clientes[0], empleado1]
for u in usuarios_variados:
    u.saludar()