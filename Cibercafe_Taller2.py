# Definimos la clase Cliente: para crear clientes del cibercafé
class Cliente:

    # Constructor: se ejecuta automáticamente al crear un cliente nuevo
    def __init__(self, nombre, documento, telefono):
        # self representa "este objeto en particular"
        self.nombre = nombre          # Guarda el nombre del cliente
        self.documento = documento    # Guarda el documento de identidad
        self.telefono = telefono      # Guarda el número de teléfono
        self.tiempo_uso = 0           # Empieza en 0, aún no ha usado ningún computador
        self.saldo_pagar = 0          # Empieza en 0, aún no debe nada

    # Método: simula el registro del cliente
    def registrarse(self):
        print(f"Cliente {self.nombre} registrado con documento {self.documento}.")

    # Método: simula que el cliente inicia sesión en una computadora
    def iniciar_sesion(self):
        print(f"{self.nombre} ha iniciado sesión en un computador.")

    # Método: simula que el cliente termina de usar el computador
    def finalizar_sesion(self, minutos, precio_por_minuto):
        self.tiempo_uso += minutos                        # Suma los minutos usados al total acumulado
        self.saldo_pagar += minutos * precio_por_minuto    # Calcula y suma lo que debe pagar
        print(f"{self.nombre} finalizó sesión. Tiempo total: {self.tiempo_uso} min. Saldo: ${self.saldo_pagar}")

    # Método: simula que el cliente pide imprimir hojas
    def solicitar_impresion(self, hojas):
        print(f"{self.nombre} solicitó imprimir {hojas} hoja(s).")

    # Método: simula el pago del cliente
    def realizar_pago(self):
        print(f"{self.nombre} pagó ${self.saldo_pagar}. Saldo actual: $0")
        self.saldo_pagar = 0    # Reinicia el saldo a 0 porque ya pagó

    # Método especial: define qué se muestra cuando hacemos print(objeto)
    # Sin esto, Python mostraría algo como <__main__.Cliente object at 0x...>
    def __str__(self):
        return (f"Cliente: {self.nombre} | Doc: {self.documento} | Tel: {self.telefono} "
                f"| Tiempo uso: {self.tiempo_uso} min | Saldo: ${self.saldo_pagar}")


# Creamos un objeto de la clase Cliente
# Python llama automáticamente a __init__ con estos tres datos
cliente1 = Cliente("Ana Torres", "1032456789", "3105551234")

# Como definimos __str__, esto imprime los datos
print(cliente1)