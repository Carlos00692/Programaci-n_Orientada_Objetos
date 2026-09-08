class Cliente:
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono


class Computadora:
    def __init__(self, numero_equipo, sistema_operativo, precio_hora):
        self.numero_equipo = numero_equipo
        self.sistema_operativo = sistema_operativo
        self.precio_hora = precio_hora
        self.estado = "Disponible"


class Sesion:
    def __init__(self, cliente, computadora):
        self.cliente = cliente
        self.computadora = computadora
        self.tiempo_uso = 0
        self.saldo_pagar = 0

    def sumar_tiempo(self, horas):
        self.tiempo_uso += horas
        self.saldo_pagar += horas * self.computadora.precio_hora

    def descripcion(self):
        return (f"Cliente: {self.cliente.nombre} | "
                f"Equipo: {self.computadora.numero_equipo} | "
                f"Tiempo: {self.tiempo_uso}h | "
                f"Saldo: ${self.saldo_pagar}")


def mostrar_lista(lista):
    for sesion in lista:
        print(sesion.descripcion())


# ============================================================
# Taller 4 - CRUD sobre la lista de Sesiones
# ============================================================

# Datos base para crear las sesiones iniciales
cliente1 = Cliente("Ana Pérez", "1-2345-6789", "8888-1234")
cliente2 = Cliente("Luis Gómez", "2-3456-7890", "8888-5678")
cliente3 = Cliente("María Rojas", "3-4567-8901", "8888-9012")

pc1 = Computadora("PC-01", "Windows 11", 500)
pc2 = Computadora("PC-02", "Linux Mint", 400)
pc3 = Computadora("PC-03", "Windows 11", 500)

sesion1 = Sesion(cliente1, pc1)
sesion1.sumar_tiempo(2)

sesion2 = Sesion(cliente2, pc2)
sesion2.sumar_tiempo(3)

sesion3 = Sesion(cliente3, pc3)
sesion3.sumar_tiempo(1)

sesiones = [sesion1, sesion2, sesion3]

print("--- Lista inicial ---")
mostrar_lista(sesiones)

# ---------- CREATE (Crear) ----------
cliente4 = Cliente("Pedro Solano", "4-5678-9012", "8888-3456")
pc4 = Computadora("PC-04", "Windows 11", 450)
sesion4 = Sesion(cliente4, pc4)
sesion4.sumar_tiempo(4)
sesiones.append(sesion4)

cliente5 = Cliente("Carla Vindas", "5-6789-0123", "8888-7890")
pc5 = Computadora("PC-05", "Linux Mint", 400)
sesion5 = Sesion(cliente5, pc5)
sesion5.sumar_tiempo(2)
sesiones.append(sesion5)

print("\n--- CREATE: lista después de agregar Pedro y Carla ---")
mostrar_lista(sesiones)

# ---------- READ (Leer) ----------
print("\n--- READ: se recorre y muestra la lista completa ---")
mostrar_lista(sesiones)

# ---------- UPDATE (Actualizar) ----------
for sesion in sesiones:
    if sesion.computadora.numero_equipo == "PC-02":
        sesion.sumar_tiempo(1)
        break

print("\n--- UPDATE: lista después de sumarle 1 hora a PC-02 ---")
mostrar_lista(sesiones)

# ---------- DELETE (Borrar) ----------
for sesion in sesiones:
    if sesion.computadora.numero_equipo == "PC-05":
        sesiones.remove(sesion)
        break

print("\n--- DELETE: lista después de eliminar la sesión de PC-05 ---")
mostrar_lista(sesiones)