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

from django.shortcuts import render, HttpResponse
from .models import Périmètre, Fichier_mansuelle
import pandas as pd

def save_data(request):
    if request.method == 'POST':
        excel_file = request.FILES.get("excel_file")
        if excel_file:
            # Charger le fichier Excel dans un DataFrame Pandas
            df = pd.read_excel(excel_file, decimal=',')

            # Convertir les colonnes nécessaires en nombres flottants
            numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne', 'Production',
                               'Prélèvement ou consommation interne', 'Prélèvements pour la Consommation autres périmètres',
                               'Pertes', 'Expédition vers TRC', 'Livraison']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

            # Extraction des valeurs de région, mois et année pour toutes les lignes
            region_name = df.iloc[0, 12]
            region = Region.objects.get_or_create(nom=region_name)[0]
            mois = df.iloc[0, 13]
            annee = df.iloc[0, 14]

            for index, row in df.iloc[1:-1].iterrows():
                perimetre_name = row['Périmètre']
                perimetre, created = Périmètre.objects.get_or_create(nom=perimetre_name, region=region)

                fichier_mansuelle = Fichier_mansuelle(
                    mois=mois,
                    annee=annee,
                    stock_ini=row['Stock Initial'],
                    Apport_consommation=row['Apports pour Consommation Interne'],
                    produit=row['Production'],
                    consomme=row['Prélèvement ou consommation interne'],
                    preleve=row['Prélèvements pour la Consommation autres périmètres'],
                    pertes=row['Pertes'],
                    expedie=row['Expédition vers TRC'],
                    laivraison=row['Livraison'],
                    densite=row['Densite'],
                    périmètre=perimetre,
                )
                fichier_mansuelle.save()

            return HttpResponse('Data saved to database.')
        else:
            return HttpResponse('No file uploaded.')
    else:
        return render(request, 'application/page_acceuil.html', {})
"""
from django.shortcuts import render, HttpResponse
from .models import Périmètre, Fichier_mansuelle
import pandas as pd

def save_data(request):
    if request.method == 'POST':
        excel_file = request.FILES.get("excel_file")
        if excel_file:
            # Charger le fichier Excel dans un DataFrame Pandas
            df = pd.read_excel(excel_file, decimal=',')

            # Convertir les colonnes nécessaires en nombres flottants
            numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne', 'Production',
                               'Prélèvement ou consommation interne', 'Prélèvements pour la Consommation autres périmètres',
                               'Pertes', 'Expédition vers TRC', 'Livraison']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

            # Extraction des valeurs de région, mois et année depuis le DataFrame
            region = df.iloc[1, 12]
            mois = df.iloc[1, 13]
            annee = df.iloc[1, 14]

            for index, row in df.iloc[1:-1].iterrows():
                perimetre, created = Périmètre.objects.get_or_create(nom=row['Périmètre'])

                fichier_mansuelle = Fichier_mansuelle(
                    mois=mois,
                    annee=annee,
                    stock_ini=row['Stock Initial'],
                    Apport_consommation=row['Apports pour Consommation Interne'],
                    produit=row['Production'],
                    consomme=row['Prélèvement ou consommation interne'],
                    preleve=row['Prélèvements pour la Consommation autres périmètres'],
                    pertes=row['Pertes'],
                    expedie=row['Expédition vers TRC'],
                    laivraison=row['Livraison'],
                    densite=row['Densite'],
                    périmètre=perimetre,
                )
                fichier_mansuelle.save()

            return HttpResponse('Data saved to database.')
        else:
            return HttpResponse('No file uploaded.')
    else:
        return render(request, 'application/page_acceuil.html', {})



from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import pandas as pd
from .models import Périmètre, Fichier_mansuelle

def index(request):
    if request.method == "GET":
        upload_form = UploadFileForm()
        return render(request, 'application/page_acceuil.html', {'upload_form': upload_form})
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
            return render(request, 'page_resultat_verifier.html', {'excel_file': excel_file})
            # Aller à la page page_resultat_verifier.html si le test est réussi
        else:
            return render(request, 'page_resultat_non_verifier.html', {'excel_file': excel_file})
            # Aller à la page page_resultat_non_verifier.html si le test échoue

def save_data(request):
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            excel_file = request.FILES['excel_file']
            # Charger le fichier Excel dans un DataFrame Pandas
            df = pd.read_excel(excel_file, decimal=',')

            # Convertir les colonnes nécessaires en nombres flottants
            numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne', 'Production',
                               'Prélèvement ou consommation interne', 'Prélèvements pour la Consommation autres périmètres',
                               'Pertes', 'Expédition vers TRC', 'Livraison']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

            # Récupérer les valeurs de région, mois et année depuis la dataframe
            region = df.iloc[1, 12]  # Supposons que la région soit à la ligne 2, colonne 13
            mois = df.iloc[1, 13]    # Supposons que le mois soit à la ligne 2, colonne 14
            annee = df.iloc[1, 14]   # Supposons que l'année soit à la ligne 2, colonne 15

            # Parcourir les données de la dataframe à partir de la deuxième ligne jusqu'à l'avant-dernière ligne
            for index, row in df.iloc[1:-1].iterrows():
                # Récupérer l'objet Perimetre correspondant à la région depuis la base de données
                perimetre, created = Périmètre.objects.get_or_create(nom=region)

                fichier_mansuelle = Fichier_mansuelle(
                    mois=mois,
                    annee=annee,
                    stock_ini=row['Stock Initial'],
                    Apport_consommation=row['Apports pour Consommation Interne'],
                    produit=row['Production'],
                    consomme=row['Prélèvement ou consommation interne'],
                    preleve=row['Prélèvements pour la Consommation autres périmètres'],
                    pertes=row['Pertes'],
                    expedie=row['Expédition vers TRC'],
                    laivraison=row['Livraison'],
                    densite=row['Densite'],
                    périmètre=perimetre,
                )
                fichier_mansuelle.save()

            return HttpResponse('Data saved to database.')
        else:
            # Si le formulaire n'est pas valide, revenir à la page d'accueil avec le formulaire et les erreurs
            return render(request, 'page_acceuil.html', {'upload_form': upload_form})
    else:
        # Si la méthode de la requête n'est pas POST, renvoyer une réponse appropriée (par exemple, redirection)
        return HttpResponse('Méthode non autorisée pour cette vue.')


import os
import tempfile
import pandas as pd
from django.shortcuts import render, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Fichier_mansuelle, Périmètre

def index(request):
    if request.method == "GET":
        return render(request, 'application/page_acceuil.html', {})
    elif request.method == "POST":
        excel_file = request.FILES["excel_file"]

        # Save the uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=True)
        temp_file.write(excel_file.read())
        temp_file.flush()

        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(temp_file.name, decimal=',')

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
            # Passer le nom du fichier temporaire à la vue save_data
            return render(request, 'page_resultat_verifier.html', {'temp_file_name': temp_file.name})
        else:
            return render(request, 'page_resultat_non_verifier.html', {'temp_file_name': temp_file.name})

def save_data(request):
    if request.method == 'POST':
        temp_file_name = request.POST.get('temp_file_name')
        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(temp_file_name, decimal=',')

        # Convertir les colonnes nécessaires en nombres flottants
        numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne', 'Production',
                           'Prélèvement ou consommation interne', 'Prélèvements pour la Consommation autres périmètres',
                           'Pertes', 'Expédition vers TRC', 'Livraison']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Récupérer les valeurs de région, mois et année depuis la dataframe
        region = df.iloc[1, 12]  # Supposons que la région soit à la ligne 2, colonne 13
        mois = df.iloc[1, 13]    # Supposons que le mois soit à la ligne 2, colonne 14
        annee = df.iloc[1, 14]   # Supposons que l'année soit à la ligne 2, colonne 15

        # Parcourir les données de la dataframe à partir de la deuxième ligne jusqu'à l'avant-dernière ligne
        for index, row in df.iloc[1:-1].iterrows():
            # Récupérer l'objet Perimetre correspondant à la région depuis la base de données
            perimetre, created = Périmètre.objects.get_or_create(nom=region)

            fichier_mansuelle = Fichier_mansuelle(
                mois=mois,
                annee=annee,
                stock_ini=row['Stock Initial'],
                Apport_consommation=row['Apports pour Consommation Interne'],
                produit=row['Production'],
                consomme=row['Prélèvement ou consommation interne'],
                preleve=row['Prélèvements pour la Consommation autres périmètres'],
                pertes=row['Pertes'],
                expedie=row['Expédition vers TRC'],
                laivraison=row['Livraison'],
                densite=row['Densite'],
                périmètre=perimetre,
            )
            fichier_mansuelle.save()

        return HttpResponse('Data saved to database.')
    else:
        # Si la méthode de la requête n'est pas POST, renvoyer à la page d'accueil
        return render(request, 'application/page_acceuil.html', {})


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
            return render(request, 'page_resultat_verifier.html', {'excel_file': excel_file})
            # Aller à la page page_resultat_verifier.html si le test est réussi
        else:
            return render(request, 'page_resultat_non_verifier.html', {'excel_file': excel_file})
            # Aller à la page page_resultat_non_verifier.html si le test échoue

def save_data(request, excel_file):
    if request.method == 'POST':
        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(excel_file, decimal=',')

        # Convertir les colonnes nécessaires en nombres flottants
        numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne', 'Production',
                           'Prélèvement ou consommation interne', 'Prélèvements pour la Consommation autres périmètres',
                           'Pertes', 'Expédition vers TRC', 'Livraison']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Récupérer les valeurs de région, mois et année depuis la dataframe
        region = df.iloc[1, 12]  # Supposons que la région soit à la ligne 2, colonne 13
        mois = df.iloc[1, 13]    # Supposons que le mois soit à la ligne 2, colonne 14
        annee = df.iloc[1, 14]   # Supposons que l'année soit à la ligne 2, colonne 15

        # Parcourir les données de la dataframe à partir de la deuxième ligne jusqu'à l'avant-dernière ligne
        for index, row in df.iloc[1:-1].iterrows():
            # Récupérer l'objet Perimetre correspondant à la région depuis la base de données
            perimetre, created = Périmètre.objects.get_or_create(nom=region)

            fichier_mansuelle = Fichier_mansuelle(
                mois=mois,
                annee=annee,
                stock_ini=row['Stock Initial'],
                Apport_consommation=row['Apports pour Consommation Interne'],
                produit=row['Production'],
                consomme=row['Prélèvement ou consommation interne'],
                preleve=row['Prélèvements pour la Consommation autres périmètres'],
                pertes=row['Pertes'],
                expedie=row['Expédition vers TRC'],
                laivraison=row['Livraison'],
                densite=row['Densite'],
                périmètre=perimetre,
            )
            fichier_mansuelle.save()

        return HttpResponse('Data saved to database.')
    else:
        # Si la méthode de la requête n'est pas POST, renvoyer à la page d'accueil
        return render(request, 'application/page_acceuil.html', {})



from django.shortcuts import render, redirect
import pandas as pd

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
            return render(request, 'page_resultat_verifier.html', {'excel_data': df})
            # Aller à la page page_resultat_verifier.html si le test est réussi
        else:
            return render(request, 'page_resultat_non_verifier.html', {'excel_data': df})
            # Aller à la page page_resultat_non_verifier.html si le test échoue



def save_data(request):
    if request.method == 'POST':
        # Récupérer les données JSON envoyées depuis la page précédente
        excel_data_json = request.POST.get('excel_data')

        # Désérialiser les données JSON en DataFrame pandas
        excel_data = pd.read_json(excel_data_json)

        # Récupérer les valeurs de région, mois et année depuis la dataframe
        region = excel_data.iloc[1, 12]  # Supposons que la région soit à la ligne 2, colonne 13
        mois = excel_data.iloc[1, 13]  # Supposons que le mois soit à la ligne 2, colonne 14
        annee = excel_data.iloc[1, 14]  # Supposons que l'année soit à la ligne 2, colonne 15

        # Parcourir les données de la dataframe à partir de la deuxième ligne jusqu'à l'avant-dernière ligne
        for index, row in excel_data.iloc[1:-1].iterrows():
            # Récupérer l'objet Perimetre correspondant à la région depuis la base de données
            perimetre, created = Périmètre.objects.get_or_create(nom=region)

            fichier_mansuelle = Fichier_mansuelle(
                mois=mois,
                annee=annee,
                stock_ini=row['Stock Initial'],
                Apport_consommation=row['Apports pour Consommation Interne'],
                produit=row['Production'],
                consomme=row['Prélèvement ou consommation interne'],
                preleve=row['Prélèvements pour la Consommation autres périmètres'],
                pertes=row['Pertes'],
                expedie=row['Expédition vers TRC'],
                laivraison=row['Livraison'],
                densite=row['Densite'],
                périmètre=perimetre,
            )
            fichier_mansuelle.save()

        return HttpResponse('Data saved to database.')
    else:
        return render(request, 'application/page_acceuil.html', {})

from django.shortcuts import render, redirect
import pandas as pd

def index(request):
    if request.method == "GET":
        return render(request, 'application/page_acceuil.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(excel_file)

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
            if test > 2 :
                test_result = False
                break

        # Rediriger en fonction du résultat du test
        if test_result:
            return render(request, 'page_resultat_verifier.html', {'excel_data': df})
            # Aller à la page page_resultat_verifier.html si le test est réussi
        else:
            return render(request, 'page_resultat_non_verifier.html', {'excel_data': df})
            # Aller à la page page_resultat_non_verifier.html si le test échoue










## fonction juste
from django.shortcuts import render, redirect
import pandas as pd

def index(request):
    if request.method == "GET":
        return render(request, 'application/page_acceuil.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # Charger le fichier Excel dans un DataFrame Pandas
        df = pd.read_excel(excel_file)

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
            if test > 2 :
                test_result = False
                break

        # Rediriger en fonction du résultat du test
        if test_result:
            return render(request, 'page_resultat_verifier.html', {'excel_data': df})
            # Aller à la page page_resultat_verifier.html si le test est réussi
        else:
            return render(request, 'page_resultat_non_verifier.html', {'excel_data': df})
            # Aller à la page page_resultat_non_verifier.html si le test échoue





def save_data(request, excel_data):
    if request.method == 'POST':
        # Récupérer les valeurs de région, mois et année depuis la dataframe
        region = excel_data.iloc[1, 12]  # Supposons que la région soit à la ligne 2, colonne 13
        mois = excel_data.iloc[1, 13]  # Supposons que le mois soit à la ligne 2, colonne 14
        annee = excel_data.iloc[1, 14]  # Supposons que l'année soit à la ligne 2, colonne 15

        # Parcourir les données de la dataframe à partir de la deuxième ligne jusqu'à l'avant-dernière ligne
        for index, row in excel_data.iloc[1:-1].iterrows():
            # Récupérer l'objet Perimetre correspondant à la région depuis la base de données
            perimetre, created = Périmètre.objects.get_or_create(nom=region)

            fichier_mansuelle = Fichier_mansuelle(
                mois=mois,
                annee=annee,
                stock_ini=row['Stock Initial'],
                Apport_consommation=row['Apports pour Consommation Interne'],
                produit=row['Production'],
                consomme=row['Prélèvement ou consommation interne'],
                preleve=row['Prélèvements pour la Consommation autres périmètres'],
                pertes=row['Pertes'],
                expedie=row['Expédition vers TRC'],
                laivraison=row['Livraison'],
                densite=row['Densite'],
                périmètre=perimetre,
            )
            fichier_mansuelle.save()

        return HttpResponse('Data saved to database.')
    else:
        return render(request, 'application/page_acceuil.html', {})


"""


