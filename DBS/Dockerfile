FROM python:3.11-slim

# Evita errores por stdin/out
ENV PYTHONUNBUFFERED=1

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    gcc g++ git && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

# Expone el puerto del servicio
EXPOSE 8000

# Comando para levantar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
