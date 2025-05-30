# Dockerfile
# Archivo de configuración para crear la imagen de Docker de la aplicación

# Usar una imagen oficial de Python como base
# Python 3.11-slim proporciona un buen equilibrio entre tamaño y funcionalidad
FROM python:3.11-slim

# Establecer el directorio de trabajo en /app dentro del contenedor
# Todas las operaciones subsiguientes se realizarán desde este directorio
WORKDIR /app

# Copiar el archivo de dependencias primero para aprovechar el cache de Docker
# Esta estrategia permite reutilizar capas cacheadas si requirements.txt no cambia
COPY requirements.txt .

# Instalar las dependencias
# --no-cache-dir reduce el tamaño de la imagen al no almacenar archivos temporales de pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación al directorio de trabajo /app
# Solo copiamos los directorios necesarios para la ejecución
COPY ./backend ./backend
COPY ./database ./database
# No copiaremos .env directamente aquí; se manejará a través de docker-compose.
# Esto mejora la seguridad y flexibilidad, permitiendo diferentes configuraciones por entorno

# Exponer el puerto en el que corre la aplicación FastAPI (según tu .env es 8000)
# Esta línea es informativa para documentar qué puerto usa la aplicación,
# aunque la publicación real del puerto la gestiona docker-compose
EXPOSE 8000

# Comando para correr la aplicación ejecutando el script del servidor directamente.
# Esto permitirá que FastMCP inicie su propio servidor (probablemente Uvicorn) como esté configurado.
# El módulo backend.server contiene la lógica de inicialización del servidor
CMD ["python", "-m", "backend.server"] 