# ============================================================
# Taller 7 - Relaciones entre clases (Cibercafé)
# ============================================================
# Relaciones:
#  - Sesion --> Cliente      : ASOCIACIÓN (el cliente existe sin la sesión)
#  - Sesion --> Computadora  : ASOCIACIÓN (la computadora existe sin la sesión)
#  - Sesion *-- Impresion    : COMPOSICIÓN (la impresión no existe sin la sesión;
#                              la Sesion la crea y la guarda en su lista)


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


class Impresion:
    """
    PARTE de una Sesion: no existe por sí sola,
    siempre se crea dentro de una sesión.
    """
    def __init__(self, paginas, precio_pagina):
        self.paginas = paginas
        self.precio_pagina = precio_pagina

    def costo(self):
        return self.paginas * self.precio_pagina


class Sesion:
    def __init__(self, cliente, computadora):
        self.cliente = cliente               # asociación
        self.computadora = computadora       # asociación
        self.tiempo_uso = 0
        self.saldo_pagar = 0
        self.impresiones = []                # composición

    def sumar_tiempo(self, horas):
        self.tiempo_uso += horas
        self.saldo_pagar += horas * self.computadora.precio_hora
        print(f"Se sumaron {horas} horas. Saldo a pagar: ${self.saldo_pagar}")

    def solicitar_impresion(self, paginas, precio_pagina=50):
        # La Sesion CREA su propia Impresion (composición)
        impresion = Impresion(paginas, precio_pagina)
        self.impresiones.append(impresion)
        self.saldo_pagar += impresion.costo()
        print(f"Impresión de {paginas} páginas agregada. Saldo a pagar: ${self.saldo_pagar}")

    def total_impresiones(self):
        return sum(i.costo() for i in self.impresiones)

    def descripcion(self):
        return (f"Cliente: {self.cliente.nombre} | "
                f"Equipo: {self.computadora.numero_equipo} | "
                f"Tiempo: {self.tiempo_uso}h | "
                f"Saldo: ${self.saldo_pagar}")


# ============================================================
# Ejecución
# ============================================================

cliente = Cliente("Elena Mora", "1-1111-2222", "8888-3333")
pc = Computadora("PC-06", "Windows 11", 500)

sesion = Sesion(cliente, pc)
sesion.sumar_tiempo(2)            # 2h x $500 = $1000
sesion.solicitar_impresion(10)    # 10 páginas x $50 = $500
sesion.solicitar_impresion(4)     # 4 páginas x $50 = $200

print("\n--- Impresiones de la sesión (composición) ---")
for imp in sesion.impresiones:
    print(f"{imp.paginas} páginas -> ${imp.costo()}")

print(f"\nTotal en impresiones: ${sesion.total_impresiones()}")
print(sesion.descripcion())