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


class Livres(models.Model):
    titre = models.CharField(max_length=100, null=False)
    auteur = models.CharField(max_length=100,  null=False)
    annee_publication = models.CharField(max_length=100)
    
class Membres(models.Model):
    nom = models.CharField(max_length=100, null = False, blank= False)
    email = models.EmailField(max_length=100, null = False, blank= False)


class Emprunts(models.Model):
    id_membre = models.ForeignKey(Membres, on_delete= models.CASCADE)
    id_livre = models.ForeignKey(Livres, on_delete= models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add = True)


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