# Dockerfile SOLO para la capa de lógica/datos (clases + SQLite).
# No incluye la interfaz gráfica (Tkinter).
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cibercafe_logica.py .

# Comprobación simple: crea la tabla, guarda y lista un cliente
CMD ["python", "-c", "import cibercafe_logica as c; c.crear_tabla(); c.Cliente('Prueba','0-0000-0000','8888-0000').guardar(); c.Cliente.listar_todos()"]
