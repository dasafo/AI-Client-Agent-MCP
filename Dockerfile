# Usar una imagen oficial de Python como base
FROM python:3.11-slim

# Establecer el directorio de trabajo en /app dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación al directorio de trabajo /app
COPY ./backend ./backend
COPY ./database ./database
# No copiaremos .env directamente aquí; se manejará a través de docker-compose.

# Exponer el puerto en el que corre la aplicación FastAPI (según tu .env es 8000)
# Esta línea sigue siendo útil para informar qué puerto intenta usar la app internamente,
# aunque la publicación real la hace docker-compose.
EXPOSE 8000

# Comando para correr la aplicación ejecutando el script del servidor directamente.
# Esto permitirá que FastMCP inicie su propio servidor (probablemente Uvicorn) como esté configurado.
CMD ["python", "-m", "backend.server"] 