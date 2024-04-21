from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Fichier_mansuelle,Périmètre
from .resources import Fichier_mansuelleResource

def essay1(request):
   return render(request,'page_acceuil.html')
def essay2(request):
   return render(request,'taritemnt_mansuel.html')
def essay3(request):
   return render(request,'page_resultat_verifier.html')
def essay4(request):
   return render(request,'page_resultat_non_verifier.html')
def essay5(request):
   return render(request,'dashboard.html')
def essay6(request):
   return render(request,'login.html')
def essay7(request):
   return render(request,'creation_compt.html')
from django.shortcuts import render
from .resources import Fichier_mansuelleResource


def save_data(request):
    if request.method == 'POST':
        data_list = request.POST.getlist('data')
        for row in data_list:
            perimetre_nom = row['perimetre_nom']
            perimetre = Périmètre.objects.get(nom=perimetre_nom)
            perimetre_id = perimetre.id_périmètre

            fichier_mansuelle = Fichier_mansuelle(
                mois=row['mois'],
                annee=row['annee'],
                stock_ini=row['stock_ini'],
                Apport_consommation=row['Apport_consommation'],
                produit=row['produit'],
                consomme=row['consomme'],
                preleve=row['preleve'],
                pertes=row['pertes'],
                expedie=row['expedie'],
                laivraison=row['laivraison'],
                densite=row['densite'],
                perimetre_id=perimetre_id,
            )
            fichier_mansuelle.save()
        return HttpResponse('Data saved to database.')
    

