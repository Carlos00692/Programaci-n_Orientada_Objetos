# Cibercafé — Proyecto de Programación Orientada a Objetos

## Negocio

**Cibercafé**: un local que renta computadoras por hora, ofrece servicio de impresión y atiende clientes que llegan a usar los equipos.

## Problema que resuelve

Llevar el control de clientes, computadoras disponibles, tiempo de uso y pagos de forma manual (papel o memoria) genera errores y pérdida de información. Este proyecto modela esas entidades como clases en Python para organizar y automatizar esa información a lo largo de distintos talleres, aplicando los conceptos de la Programación Orientada a Objetos.

---

## Estructura del repositorio

| Archivo | Contenido -
|---|---|
| `Cibercafe_proyecto_completo.py` | **Proyecto principal** — integra todos los talleres (2 al 9) en un solo programa funcional. |
| `Cibercafe_Taller2.py` | Taller 2 — primera clase `Cliente` en Python. |
| `Cibercafe_Taller3.py` | Taller 3 — objetos guardados en una lista y recorridos con `for`. |
| `Cibercafe_Taller4.py` | Taller 4 — CRUD sobre una lista de `Sesion`, como archivo independiente. |
| `Cibercafe_Taller5.py` | Taller 5 — jerarquía de herencia (`Usuario` → `Cliente`/`Empleado`), independiente. |
| `Cibercafe_Taller6.py` | Taller 6 — CRUD de `Cliente` con `__str__` y polimorfismo, independiente. |
| `Cibercafe_Taller7.py` | Taller 7 — relaciones entre clases (asociación y composición), independiente. |
| `Cibercafe_Taller8.py` | Taller 8 — CRUD de `Cliente` con persistencia en SQLite, independiente. |
| `Cibercafe_Taller9.py` | Taller 9 — interfaz gráfica (Tkinter) sobre el CRUD de SQLite, independiente. |
| `cibercafe.db` | Base de datos SQLite generada por los Talleres 8 y 9. |
| `README.md` | Este documento. |

> Nota: `Cibercafe_Taller2.py` a `Cibercafe_Taller9.py` son versiones aisladas de cada ejercicio, pensadas para entregarse por separado. **`Cibercafe_proyecto_completo.py`** es la versión "oficial" del negocio, donde todo vive integrado y conectado.

---

## Evolución del proyecto por taller

### Taller 1 — De mi negocio a objetos
Se identificaron las clases del negocio: `Cliente`, `Computadora`, `Impresión`, `Empleado`, `Pago`, con sus atributos y métodos en papel (sin código todavía).

### Taller 2 — Tu primera clase en Python
Se programó la clase `Cliente` con `__init__` y un método (`registrar_cliente`).

### Taller 3 — Tus objetos en una lista
Se crearon al menos 3 objetos, se guardaron en una lista con `.append()` y se recorrieron con un `for`, mostrando cada uno con un método `descripcion()`.

### Taller 4 — Tu primer CRUD
Se detectó un problema de diseño: `tiempo_uso` y `saldo_pagar` no pertenecen al `Cliente` (un dato fijo), sino a una **Sesión** (una visita puntual). Se creó la clase `Sesion` y sobre su lista se implementó el CRUD completo:
- **Create:** se agregan nuevas sesiones con `.append()`.
- **Read:** se recorre la lista con un `for` y `descripcion()`.
- **Update:** se busca una sesión por número de equipo y se le suma tiempo (`sumar_tiempo()`).
- **Delete:** se elimina una sesión de la lista con `.remove()`.
La lista se imprime después de cada operación para ver el efecto.

### Taller 5 — La jerarquía de tu proyecto
Se creó la clase base `Usuario` (nombre, documento, teléfono, `saludar()`), de la cual heredan:
- `Cliente` — atributo propio `membresia`, método propio `ver_membresia()`.
- `Empleado` — atributo propio `salario`, método propio `cobrar_salario()`.

Ambas subclases usan `super().__init__(...)` para reutilizar el constructor de `Usuario`.

### Taller 6 — CRUD de Clientes + Polimorfismo
Se le agregó a `Cliente`:
- Un método `__str__` para mostrarlo directamente con `print()`.
- Un atributo `compras`.
- Una **sobreescritura** del método `saludar()` heredado de `Usuario` (polimorfismo): un `Cliente` saluda mencionando su membresía, mientras que `Empleado` conserva el saludo genérico de `Usuario`.

Sobre una lista de clientes se implementó el CRUD completo (crear, leer con `__str__`, actualizar sus compras, borrar uno) y se demostró el polimorfismo recorriendo una lista mixta `[Cliente, Empleado]` donde cada objeto ejecuta su propia versión de `saludar()`.

### Taller 7 — Relaciones entre clases
Se identificaron tres relaciones reales del negocio, decididas con el criterio *"¿la parte existe sin el todo?"*:

| Relación | Tipo | Justificación |
|---|---|---|
| `Sesion` → `Cliente` | Asociación | El cliente existe aunque no tenga sesiones. |
| `Sesion` → `Computadora` | Asociación | La computadora existe aunque nadie la use. |
| `Sesion` ◆— `Impresion` | **Composición** | Una impresión no existe sin su sesión: la `Sesion` la crea y la guarda en su lista `impresiones`. |

Implementación: se creó la clase `Impresion` (`paginas`, `precio_pagina`, `costo()`) y en `Sesion` se agregaron la lista `impresiones` y los métodos `solicitar_impresion()` (crea la impresión y suma su costo al saldo) y `total_impresiones()`.

### Taller 8 — CRUD de Cliente con persistencia en SQLite
Se le agregaron a `Cliente` cuatro métodos que conectan con una base de datos real (`cibercafe.db`), reemplazando el CRUD en memoria del Taller 6 por uno persistente:
- **`guardar()`** → `INSERT` (Create). Controla con `try/except` que no falle si el documento ya existe (clave primaria duplicada).
- **`listar_todos()`** → `SELECT` (Read).
- **`actualizar()`** → `UPDATE` sobre nombre, teléfono, membresía y compras (Update).
- **`eliminar()`** → `DELETE` (Delete).

La tabla `clientes` usa `documento` como `PRIMARY KEY`. Se puede verificar el resultado abriendo `cibercafe.db` en DB Browser for SQLite.

### Taller 9 — Interfaz gráfica (Tkinter)
Se construyó la clase `AppClientes` con Tkinter, que reutiliza directamente los métodos del Taller 8 sin duplicar lógica:
- Un campo `Entry` por atributo (documento, nombre, teléfono, membresía, compras).
- Botones **Guardar**, **Actualizar**, **Eliminar** y **Limpiar**, conectados a `guardar()`, `actualizar()` y `eliminar()`.
- Un `Listbox` que se refresca con `refrescar_lista()` después de cada operación, mostrando también el teléfono.
- Al hacer clic en un cliente de la lista, sus datos se cargan en los campos para poder editarlos o borrarlos.

---

## Diagrama de clases UML

El diagrama completo (clases, herencia del Taller 5 y las relaciones del Taller 7) está en `diagrama_uml.mermaid`:

```mermaid
classDiagram
    class Usuario {
        +nombre
        +documento
        +telefono
        +saludar()
    }
    class Cliente {
        +membresia
        +compras
        +registrar_cliente()
        +ver_membresia()
        +saludar()
        +__str__()
        +guardar()
        +listar_todos()
        +actualizar()
        +eliminar()
    }
    class Empleado {
        +salario
        +cobrar_salario()
    }
    class Computadora {
        +numero_equipo
        +sistema_operativo
        +precio_hora
        +estado
        +encender()
        +apagar()
        +cambiar_estado(nuevo_estado)
    }
    class Sesion {
        +cliente
        +computadora
        +tiempo_uso
        +saldo_pagar
        +impresiones
        +iniciar_sesion()
        +sumar_tiempo(horas)
        +solicitar_impresion(paginas, precio_pagina)
        +total_impresiones()
        +finalizar_sesion()
        +realizar_pago()
        +descripcion()
    }
    class Impresion {
        +paginas
        +precio_pagina
        +costo()
    }
    class AppClientes {
        +refrescar_lista()
        +guardar()
        +actualizar()
        +eliminar()
        +seleccionar_de_lista()
    }

    Usuario <|-- Cliente : herencia
    Usuario <|-- Empleado : herencia
    Sesion "*" --> "1" Cliente : asociacion
    Sesion "*" --> "1" Computadora : asociacion
    Sesion "1" *-- "0..*" Impresion : composicion
    AppClientes ..> Cliente : usa
```

---

## Jerarquía de clases (proyecto principal)

```
Usuario (clase base)
├── Cliente   (membresia, compras, ver_membresia(), saludar() sobreescrito, __str__,
│              guardar(), listar_todos(), actualizar(), eliminar())   <- SQLite (Taller 8)
└── Empleado  (salario, cobrar_salario())

Computadora   (numero_equipo, sistema_operativo, precio_hora, estado)

Sesion        (cliente, computadora, tiempo_uso, saldo_pagar, impresiones,
               iniciar_sesion(), sumar_tiempo(), solicitar_impresion(),
               total_impresiones(), finalizar_sesion(), realizar_pago(),
               descripcion())
  └── Impresion  (paginas, precio_pagina, costo())   <- composición

AppClientes   (interfaz Tkinter, Taller 9 — usa los métodos de Cliente)
```

## Cómo ejecutar

```bash
python3 Cibercafe_proyecto_completo.py
```

Esto corre, en orden: el flujo en memoria de los Talleres 2 a 7 (registro, sesiones, lista, CRUD de sesiones, herencia, polimorfismo, composición con Impresión), luego el CRUD contra SQLite del Taller 8, y al final abre la ventana de Tkinter del Taller 9 (reutiliza `cibercafe.db`).

Cada taller también puede probarse por separado ejecutando su archivo individual, por ejemplo:

```bash
python3 Cibercafe_Taller9.py
```