from django.http import HttpResponse,HttpResponseBadRequest
import pandas as pd
from .models import Fichier_mansuelle , Périmètre
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur, Fichier_mansuelle ,Périmètre,Region

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
def essay8(request):
   return render(request,'page_sauvgarde.html')


#ymchiww
def index(request):
    if request.method == "GET":
        return render(request, 'application/page_acceuil.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(excel_file, decimal=',')

        # Convertir les colonnes nécessaires en nombres flottants
        numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne', 'Production', 
                           'Prélèvement ou consommation interne', 'Prélèvements pour la Consommation autres périmètres', 
                           'Pertes', 'Expédition vers TRC', 'Livraison']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Effectuer le test sur chaque tuple, en commençant de la deuxième ligne
        test_result = True
        for index, row in df.iloc[1:-1].iterrows(): 
            # Calculer la variable test selon la formule donnée
            test = row['Stock Initial'] + row['Apports pour Consommation Interne'] + row['Production'] - row['Prélèvement ou consommation interne'] - row['Prélèvements pour la Consommation autres périmètres'] - row['Pertes'] - row['Expédition vers TRC'] - row['Livraison']
            # Vérifier si la variable test est inférieure à 1
            if test > 1:
                test_result = False
                break

        # Rediriger en fonction du résultat du test
        if test_result:
            return render(request, 'page_resultat_verifier.html')
            # Aller à la page page_resultat_verifier.html si le test est réussi
        else:
            return render(request, 'page_resultat_non_verifier.html')
            # Aller à la page page_resultat_non_verifier.html si le test échoue

def save_data(request):
    if request.method == 'POST':
        excel_file = request.FILES.get("excel_file")
        if excel_file:
            # Charger le fichier Excel dans un DataFrame Pandas
            df = pd.read_excel(excel_file, decimal=',')

            # Convertir les colonnes nécessaires en nombres flottants
            numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne',
                               'Prélèvement ou consommation interne',
                               'Prélèvements pour la Consommation autres périmètres',
                               'Pertes', 'Expédition vers TRC', 'Livraison',
                               'Stock final']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
            df.fillna(0, inplace=True)

            # Extraction des valeurs de mois et année pour la première ligne
            mois = df.iloc[0, 13]
            annee = df.iloc[0, 14]

            # Boucle à partir de la deuxième ligne jusqu'à l'avant-dernière ligne
            for index, row in df.iloc[:5].iterrows():
                perimetre_name = row['Périmètre']
                # Récupérer l'ID du périmètre en fonction de son nom
                perimetre_id = Périmètre.objects.get(nom=perimetre_name).id_périmètre

                # Calcul de la production en utilisant la formule
                production = (
                    row['Prélèvement ou consommation interne'] +
                    row['Prélèvements pour la Consommation autres périmètres'] +
                    row['Pertes'] +
                    row['Expédition vers TRC'] -
                    row['Livraison'] +
                    df.iloc[index]['Stock final'] -
                    row['Stock Initial'] -
                    row['Apports pour Consommation Interne']
                )

                fichier_mansuelle = Fichier_mansuelle(
                    mois=mois,
                    annee=annee,
                    stock_ini=row['Stock Initial'],
                    Apport_consommation=row['Apports pour Consommation Interne'],
                    produit=production,
                    consomme=row['Prélèvement ou consommation interne'],
                    preleve=row['Prélèvements pour la Consommation autres périmètres'],
                    pertes=row['Pertes'],
                    expedie=row['Expédition vers TRC'],
                    laivraison=row['Livraison'],
                    densite=row['Densite'],
                    périmètre_id=perimetre_id,  # Utilisation de l'ID du périmètre
                )
                fichier_mansuelle.save()

            return HttpResponse('Data saved to database.')
        else:
            return HttpResponse('No file uploaded.')
    else:
        return render(request, 'application/page_acceuil.html', {})



