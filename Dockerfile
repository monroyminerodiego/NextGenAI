# ===== Comandos para ejecutar docker
# docker build -t flask-d3-app . && docker run -p 10000:10000 flask-d3-app
# ==========

# Imagen base oficial de Python
FROM python:3.11-slim

# Crear y usar directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer puerto Flask (por defecto 5000)
EXPOSE 10000

# Comando para correr la app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "app:app"]
