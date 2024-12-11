
FROM python:3.10-slim
   
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du code source
COPY . .

# Exécuter les commandes de migration et collectstatic avant de démarrer l'application
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:80"]