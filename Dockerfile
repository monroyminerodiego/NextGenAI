# ===== Comandos para ejecutar docker
# docker build -t visualization-badges . && docker run -p 10000:10000 visualization-badges
# ==========

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.enableCORS=false"]
