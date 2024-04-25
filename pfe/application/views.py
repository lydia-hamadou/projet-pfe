from django.http import HttpResponse
import pandas as pd
from .models import Fichier_mansuelle , Périmètre
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur

logging.basicConfig(filename='app.log', level=logging.ERROR)

from django.contrib.auth import authenticate

from django.shortcuts import render
from .models import Utilisateur

def login(request):
    nom_utilisateur_invalid = False
    mot_de_passe_invalid = False

    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')

        try:
            utilisateur = Utilisateur.objects.get(nom=nom)
            if utilisateur.password == password:
                # Si le nom d'utilisateur et le mot de passe correspondent, redirigez vers la page d'accueil
                return render(request, 'page_acceuil.html')
            else:
                # Si le mot de passe est incorrect, définir mot_de_passe_invalid sur True
                mot_de_passe_invalid = True
        except Utilisateur.DoesNotExist:
            # Si l'utilisateur n'existe pas, définir nom_utilisateur_invalid sur True
            nom_utilisateur_invalid = True

    return render(request, 'login.html', {'nom_utilisateur_invalid': nom_utilisateur_invalid, 'mot_de_passe_invalid': mot_de_passe_invalid})


    
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



def upload_and_test_data(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        if df.empty:
            raise ValueError("Excel file is empty or contains no data")
        print(df.columns)

      
        request.data = df.to_dict(orient='records')
        all_rows_pass = True
        for index, row in df.iterrows():
            mois = row['Mois']
            annee = row['Année']
            stock_ini = row['Stock Initial']
            apport_consommation = row['Apports pour Consommation']
            produit = row['Production']
            consomme = row['Consommations']
            preleve = row['Prélèvements ou Production']
            pertes = row['Pertes']
            expedie = row['Expédition vers TRC']
            livraison = row['Livraison']

            
            production = stock_ini + expedie + pertes + preleve + consomme - apport_consommation

            
            if production != produit:
                all_rows_pass = False
                break

        
        if all_rows_pass:
            return render(request, 'page_resultat_verifier.html', {'data': request.data})
        else:
            
            return render(request, 'page_resultat_non_verifier.html', {'data': request.data})

   
    return render(request, 'taritemnt_mansuel.html')

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
    

