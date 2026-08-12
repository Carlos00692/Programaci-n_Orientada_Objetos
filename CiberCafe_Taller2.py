class Cliente:
    def __init__(self, nombre, documento, telefono, tiempo_uso, saldo_pagar):
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
        self.tiempo_uso = tiempo_uso
        self.saldo_pagar = saldo_pagar

    def registrar_cliente(self):
        print(f"Cliente {self.nombre} registrado con éxito.")
        print(f"Datos registrados.")

obj = Cliente("Ana Pérez", "1-2345-6789", "8888-1234", "2 horas", 1500)
obj.registrar_cliente()
print("nombre:", obj.nombre)
print("documento:", obj.documento)
print("telefono:", obj.telefono)
print("tiempo_uso:", obj.tiempo_uso)
print("saldo_pagar:", obj.saldo_pagar)