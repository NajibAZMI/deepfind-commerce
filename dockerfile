# Utilisation d'une image Python
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Installer les dépendances
RUN pip install flask keras tensorflow

# Exposer le port
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
