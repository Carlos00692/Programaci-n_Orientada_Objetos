# ============================================================
# Taller 5 - Jerarquía de herencia (Cibercafé)
# ============================================================

class Usuario:
    """
    Clase BASE: agrupa lo que TODA persona relacionada al cibercafé
    tiene en común, sin importar si es cliente o empleado.
    """
    def __init__(self, nombre, documento, telefono):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono

    def saludar(self):
        print(f"Hola, soy {self.nombre} (documento: {self.documento}).")


class Cliente(Usuario):
    """
    Subclase 1: hereda de Usuario y agrega lo propio de un cliente.
    """
    def __init__(self, nombre, documento, telefono, saldo_pendiente):
        # Llama al constructor de la clase base para no repetir código
        super().__init__(nombre, documento, telefono)
        self.saldo_pendiente = saldo_pendiente   # atributo PROPIO de Cliente

    def ver_saldo(self):
        # método PROPIO de Cliente
        print(f"{self.nombre} tiene un saldo pendiente de ${self.saldo_pendiente}.")


class Empleado(Usuario):
    """
    Subclase 2: hereda de Usuario y agrega lo propio de un empleado.
    """
    def __init__(self, nombre, documento, telefono, salario):
        # Llama al constructor de la clase base para no repetir código
        super().__init__(nombre, documento, telefono)
        self.salario = salario   # atributo PROPIO de Empleado

    def cobrar_salario(self):
        # método PROPIO de Empleado
        print(f"{self.nombre} recibió su salario de ${self.salario}.")


# ============================================================
# Se crea un objeto de cada subclase
# ============================================================

cliente1 = Cliente("Ana Pérez", "1-2345-6789", "8888-1234", saldo_pendiente=1500)
empleado1 = Empleado("Luis Gómez", "2-3456-7890", "8888-5678", salario=350000)

print("=== Lo que AMBOS comparten (heredado de Usuario) ===")
cliente1.saludar()
empleado1.saludar()

print("\n=== Lo que cada uno tiene de PROPIO ===")
cliente1.ver_saldo()        # solo Cliente lo tiene
empleado1.cobrar_salario()  # solo Empleado lo tiene