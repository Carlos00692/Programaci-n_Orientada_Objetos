class Cliente:
    # __init__ es el "constructor": se ejecuta automáticamente al crear un objeto Cliente
    # self representa al propio objeto que se está creando
    def __init__(self, nombre, documento, telefono, tiempo_uso, saldo_pagar):
        self.nombre = nombre            # Guarda el nombre del cliente en el objeto
        self.documento = documento      # Guarda el número de documento de identidad
        self.telefono = telefono        # Guarda el número de teléfono
        self.tiempo_uso = tiempo_uso    # Guarda cuánto tiempo ha usado el servicio
        self.saldo_pagar = saldo_pagar  # Guarda el monto pendiente de pago

    # Método: acción que puede realizar un objeto Cliente
    def registrar_cliente(self):
        # Imprime un mensaje de confirmación usando el nombre guardado en el objeto
        print(f"Cliente {self.nombre} registrado con éxito.")
        print(f"Datos registrados.")

# Se crea un objeto de la clase Cliente
# Estos valores se envían al método __init__ y quedan guardados en el objeto "obj"
obj = Cliente("Ana Pérez", "1-2345-6789", "8888-1234", "2 horas", 1500)

# Se llama al método registrar_cliente() del objeto obj
# Esto ejecuta el método (el print del mensaje)
obj.registrar_cliente()

# Se muestran todos los atributos del objeto usando print
# obj.nombre, obj.documento, etc. acceden a los datos guardados en el objeto
print("NOMBRE:", obj.nombre)
print("DOCUMENTO:", obj.documento)
print("TELÉFONO:", obj.telefono)
print("TIEMPO DE USO:", obj.tiempo_uso)
print("SALDO A PAGAR:", obj.saldo_pagar)