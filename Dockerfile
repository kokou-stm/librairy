# Utiliser une image Python optimisée pour la production
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . /app/

# Exposer le port par défaut de Django
EXPOSE 8000

# Commande pour collecter les fichiers statiques et lancer le serveur
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn librairy.wsgi:application --bind 0.0.0.0:8000"]
