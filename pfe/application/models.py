from django.db import models

# Create your models here.
class Region(models.Model):
    id_region = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=255)

class Périmètre(models.Model):
    id_périmètre = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Prévision_perimetre(models.Model):
   
    id = models.AutoField(primary_key=True)
    mois = models.IntegerField()
    annee = models.IntegerField()
    prévision = models.DecimalField(max_digits=10, decimal_places=2)
    périmètre = models.ForeignKey(Périmètre, on_delete=models.CASCADE)

class Fichier_mansuelle(models.Model):

    id_fichier = models.AutoField(primary_key=True)
    mois = models.IntegerField()
    annee = models.IntegerField()
    stock_ini = models.DecimalField(max_digits=10, decimal_places=2)
    Apport_consommation = models.DecimalField(max_digits=10, decimal_places=2)
    produit = models.DecimalField(max_digits=10, decimal_places=2)
    consomme = models.DecimalField(max_digits=10, decimal_places=2)
    preleve = models.DecimalField(max_digits=10, decimal_places=2)
    pertes = models.DecimalField(max_digits=10, decimal_places=2)
    expedie = models.DecimalField(max_digits=10, decimal_places=2)
    livraison = models.DecimalField(max_digits=10, decimal_places=2)
    densite = models.DecimalField(max_digits=3, decimal_places=1)
    périmètre = models.ForeignKey(Périmètre, on_delete=models.CASCADE)

class Utilisateur(models.Model):
    id_utilisateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

class Visualisation(models.Model):
    id_visualisation = models.AutoField(primary_key=True)
    date = models.DateField()
    visualisation = models.CharField(max_length=255)

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    visualisation = models.ForeignKey(Visualisation, on_delete=models.CASCADE)
    date = models.DateField()
    commentaire = models.TextField()
    class Meta:
        unique_together = (('utilisateur', 'visualisation'),)



