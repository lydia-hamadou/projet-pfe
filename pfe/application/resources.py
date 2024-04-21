from import_export import resources
from .models import Fichier_mansuelle


class Fichier_mansuelleResource(resources.ModelResource):
    class Meta:
        model = Fichier_mansuelle
