# Integrantes: Diego Henríquez y
# Sección: OCY1102

FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python create_db.py
EXPOSE 5000
CMD ["python", "vulnerable_flask_app.py"]