
FROM python:3.10
#ENV PYTHONBUFFERED 1

# Install pip
#RUN apt-get install -y python3-pip
# Mettre à jour et installer les dépendances nécessaires
   
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Commande de démarrage avec Gunicorn pour un environnement de production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "librairy.wsgi:application"]
