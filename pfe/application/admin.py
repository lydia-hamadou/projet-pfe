from django.contrib import admin
from .models import Region ,Périmètre ,Prévision_perimetre, Fichier_mansuelle,Utilisateur ,Visualisation,Commentaire
from .models import Fichier_mansuelle

admin.site.register(Region)
admin.site.register(Périmètre)
admin.site.register(Prévision_perimetre)
admin.site.register(Fichier_mansuelle)
admin.site.register(Utilisateur)
admin.site.register(Commentaire)
admin.site.register(Visualisation)



