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
    def __init__(self, cliente, computadora, horas):
        self.cliente = cliente
        self.computadora = computadora
        self.tiempo_uso = horas
        self.saldo_pagar = horas * computadora.precio_hora

    def descripcion(self):
        # Método que devuelve un texto con los datos de la sesión
        return (f"Cliente: {self.cliente.nombre} | "
                f"Equipo: {self.computadora.numero_equipo} | "
                f"Tiempo: {self.tiempo_uso}h | "
                f"Saldo: ${self.saldo_pagar}")


# ============================================================
# Taller 3 - Lista de objetos Sesion
# ============================================================

# Clientes y computadoras de apoyo (necesarios para crear una Sesion)
cliente1 = Cliente("Ana Pérez", "1-2345-6789", "8888-1234")
cliente2 = Cliente("Luis Gómez", "2-3456-7890", "8888-5678")
cliente3 = Cliente("María Rojas", "3-4567-8901", "8888-9012")

pc1 = Computadora("PC-01", "Windows 11", 500)
pc2 = Computadora("PC-02", "Linux Mint", 400)
pc3 = Computadora("PC-03", "Windows 11", 500)

# 1. Se crean al menos 3 objetos distintos de la clase Sesion
sesion1 = Sesion(cliente1, pc1, 2)   # Ana usó PC-01 por 2 horas
sesion2 = Sesion(cliente2, pc2, 3)   # Luis usó PC-02 por 3 horas
sesion3 = Sesion(cliente3, pc3, 1)   # María usó PC-03 por 1 hora

# 2. Se guardan en una lista usando append()
sesiones = []
sesiones.append(sesion1)
sesiones.append(sesion2)
sesiones.append(sesion3)

# 3. Se recorre la lista con un for y se muestra cada objeto
print("=== SESIONES REGISTRADAS ===")
for sesion in sesiones:
    print(sesion.descripcion())