# Indico qué lenguaje y versión quiero
FROM python:3.11-slim

# Establezco la carpeta de trabajo (backend en este caso)
WORKDIR /app/backend

# Copio las dependencias
COPY requirements.txt .

# Instalo el requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Se copia todo el código en el contenedor
COPY . .

# Establezco las variables de entorno
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=development

# Expongo el puerto para el navegador
EXPOSE 5000

# Ejecuto la app
CMD ["python", "-m", "flask", "run"]