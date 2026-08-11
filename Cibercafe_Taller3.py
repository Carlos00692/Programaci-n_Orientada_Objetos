class Distribucion_PC:
    def __init__(self, cliente, pc_asignado):
        self.cliente = cliente
        self.pc_asignado = pc_asignado

    def descripcion(self):
        return f"Cliente: {self.cliente} - PC asignado: {self.pc_asignado}"


lista = []
lista.append(Distribucion_PC("Juan Pérez", "PC-01"))
lista.append(Distribucion_PC("Ana Gómez", "PC-02"))
lista.append(Distribucion_PC("Luis Rojas", "PC-03"))

for obj in lista:
    print(obj.descripcion())