class Cliente:
    # __init__ es el "constructor": se ejecuta automáticamente al crear un objeto Cliente
    # self representa al propio objeto que se está creando
    def __init__(self, nombre, documento, telefono, tiempo_uso, saldo_pagar):
        self.nombre = nombre             
        self.documento = documento      
        self.telefono = telefono       
        self.tiempo_uso = tiempo_uso   
        self.saldo_pagar = saldo_pagar  

    # Método: acción que puede realizar un objeto Cliente
    def registrar_cliente(self):
        # Imprime un mensaje de confirmación usando el nombre guardado en el objeto
        print(f"Cliente {self.nombre} registrado con éxito.")
        print(f"DATOS REGISTRADOS:")
        print(f"Nombre: {self.nombre}")
        print(f"Documento: {self.documento}")
        print(f"Teléfono: {self.telefono}")
        print(f"Tiempo de uso: {self.tiempo_uso}")
        print(f"Saldo por pagar: {self.saldo_pagar}")

# Se crea un objeto (instancia) de la clase Cliente
# Estos valores se envían al método __init__ y quedan guardados en el objeto "obj"
obj = Cliente("Ana Pérez", "1-2345-6789", "8888-1234", "2 horas", 1500)

# Se llama al método registrar_cliente() del objeto obj
# Esto ejecuta la acción definida dentro del método (el print del mensaje)
obj.registrar_cliente()

# Se muestran todos los atributos del objeto usando print
# obj.nombre, obj.documento, etc. acceden a los datos guardados en el objeto
print(obj.nombre, obj.documento, obj.telefono, obj.tiempo_uso, obj.saldo_pagar)