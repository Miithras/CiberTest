# Usamos una imagen base de Python ligera
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los requerimientos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Ejecutamos el script para crear la base de datos inicial
RUN python create_db.py

# Exponemos el puerto 5000 (puerto por defecto de Flask)
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "vulnerable_flask_app.py"]