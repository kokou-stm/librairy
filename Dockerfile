FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Démarrer le serveur
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "monprojet.wsgi:application"]