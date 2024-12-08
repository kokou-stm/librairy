from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6, unique=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def generate_code(self):
        self.code = str(uuid.uuid4().int)[:6]
        self.save()


class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    numero_de_carte = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Numéro de carte étudiant
    phone = models.CharField(max_length=15, blank=True, null=True)  # Téléphone
    nom = models.CharField(max_length=100, null = False, blank= False)
    email = models.EmailField(max_length=100, null = False, blank= False)
   

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Book(models.Model):
    titre = models.CharField(max_length=100, null=False)
    auteur = models.CharField(max_length=100,  null=False)
    annee_publication = models.DateField()
    description= models.CharField(null=True, blank=True)
    image = models.FileField(upload_to='images')
    
    def __str__(self):
        return self.titre

class Emprunts(models.Model):
    STATUS = {
    "O":"Rendu",
    'C': 'en_cours',
    'N': 'Non_rendu'
    } 
    id_membre = models.ForeignKey(Membre, on_delete= models.CASCADE)
    id_livre = models.ForeignKey(Book, on_delete= models.CASCADE)
    date_emprunt = models.DateField(auto_now_add = True)
    date_retour = models.DateField(blank=True, null=True)
    date_rendu = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='C')

    def __str__(self):
        return self.id_membre.nom + self.id_livre.titre


'''Création des tables
Créez les tables suivantes avec les colonnes spécifiées :
• Table : livres
o id_livre (INTEGER, clé primaire)
o titre (VARCHAR(100), non nul)
o auteur (VARCHAR(100), non nul)
o annee_publication (INTEGER, non nul)
• Table : membres
o id_membre (INTEGER, clé primaire)
o nom (VARCHAR(100), non nul)
o email (VARCHAR(100), non nul)
• Table : emprunts
o id_emprunt (INTEGER, clé primaire)
o id_membre (INTEGER, clé étrangère vers membres.id_membre)
o id_livre (INTEGER, clé étrangère vers livres.id_livre)
o date_emprunt (DATE, non nul)
o date_retour (DATE)'''