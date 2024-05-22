from django.http import HttpResponse
import pandas as pd
from .models import Fichier_mansuelle , Périmètre
import logging
from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import A4, landscape
from django.contrib import messages
from .models import Utilisateur, Fichier_mansuelle ,Périmètre,Region,Prévision_perimetre
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from django.db.models import Sum, F, FloatField,Value
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.db.models import Sum, F, Value, FloatField
from django.db.models.functions import Coalesce
from openpyxl.utils import get_column_letter
from openpyxl.styles.borders import Border, Side
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .models import Périmètre, Fichier_mansuelle
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os



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
"""

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login

@login_required(login_url='application:acceuil')
def login(request):
    if request.user.is_authenticated:
        request.session.flush()
        return redirect('application:acceuil')

    nom_utilisateur_invalid = False
    mot_de_passe_invalid = False

    if request.method == 'POST':
        nom = request.POST.get('nom')
        password = request.POST.get('password')

        user = authenticate(request, username=nom, password=password)  # Authentification avec Django

        if user is not None:
            login(request, user)  # Connexion de l'utilisateur
            return redirect('application:acceuil')
        else:
            mot_de_passe_invalid = True  # Mot de passe incorrect

    return render(request, 'login.html', {'nom_utilisateur_invalid': nom_utilisateur_invalid, 'mot_de_passe_invalid': mot_de_passe_invalid})

"""
def acceuil(request):
   return render(request,'page_acceuil.html')
def taritemnt_mansuel(request):
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
def traitement_p1(request):
   return render(request,'traitement_p1.html')
def traitement_annuel(request):
   return render(request,'traitement_annuel.html')
def dashboard(request):
   return render(request,'dashboard.html')
def page_reponce(request):
   return render(request,'page_réponce.html')


""" entrain de modifier elle est juste 
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
"""
"""
#probléme de pas de fichier est régler 
import pandas as pd
from django.shortcuts import render

def index(request):
    if request.method == "POST":
        if "excel_file" in request.FILES:
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
            else:
                return render(request, 'page_resultat_non_verifier.html')

        else:  # Gérer le cas où aucun fichier n'est sélectionné
            return render(request, 'page_acceuil.html', {'error': "Veuillez sélectionner un fichier."})

    else:
        return render(request, 'page_acceuil.html')





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

            return render(request, 'page_fichier_sauvgarder.html')
        else:
            return HttpResponse('No file uploaded.')
    else:
        return render(request, 'application/page_acceuil.html', {})

"""
def page_resultat_verifier(request):
    if request.method == 'POST':
        return save_data(request)  # Appeler save_data si le formulaire est soumis
    else:
        excel_file_path = request.session.get('excel_file_path')
        if not excel_file_path:
            return redirect('index')  # Rediriger si aucun fichier n'est trouvé
        return render(request, 'page_resultat_verifier.html', {'excel_file_path': excel_file_path})


def index(request):
    if request.method == "POST":
        if "excel_file" in request.FILES:
            excel_file = request.FILES["excel_file"]
            
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)  # Construisez le chemin complet
            request.session['excel_file_path'] = file_path  

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
               request.session['excel_file_path'] = file_path
               return redirect('application:page_resultat_verifier')
            else:
                return render(request, 'page_resultat_non_verifier.html')

        else:  # Gérer le cas où aucun fichier n'est sélectionné
            return render(request, 'page_acceuil.html', {'error': "Veuillez sélectionner un fichier."})

    else:
        return render(request, 'page_acceuil.html')

def save_data(request):
    excel_file_path = request.session.get('excel_file_path')

    if not excel_file_path:
        return render(request, 'page_acceuil.html', {'error': "Aucun fichier sélectionné."})

    try:
        df = pd.read_excel(excel_file_path, decimal=',')

        # Convertir les colonnes nécessaires en nombres flottants
        numeric_columns = ['Stock Initial', 'Apports pour Consommation Interne',
                           'Prélèvement ou consommation interne',
                           'Prélèvements pour la Consommation autres périmètres',
                           'Pertes', 'Expédition vers TRC', 'Livraison',
                           'Stock final']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.fillna(0, inplace=True)

        # Extraction des valeurs de mois et année pour la première ligne
        mois = df.iloc[0, 13]
        annee = df.iloc[0, 14]

        # Liste pour stocker les périmètres inexistants
        perimetres_inexistants = []

        for index, row in df.iloc[1:-1].iterrows():
            perimetre_name = row['Périmètre']

            try:
                perimetre = Périmètre.objects.get(nom=perimetre_name)

                # Vérification de l'existence de l'entrée
                if Fichier_mansuelle.objects.filter(mois=mois, annee=annee, périmètre=perimetre).exists():
                                        return render(request, 'page_réponce.html', {'message': "Fichier existe" , 'error': False} )
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
                    périmètre=perimetre, 
                )
                fichier_mansuelle.save()

            except Périmètre.DoesNotExist:
                perimetres_inexistants.append(perimetre_name)

        if perimetres_inexistants:
            return render(request, 'page_réponce.html', {'message': "Périmètres inexistants"}) 
        else:
            return render(request, 'page_réponce.html', {'message': "Fichier sauvegardé" ,'error': True})


    except FileNotFoundError:
        return render(request, 'page_acceuil.html', {'error': "Le fichier sélectionné n'a pas été trouvé."})

from django.db.models import Sum, F
from django.db.models.functions import Coalesce 
from django.shortcuts import render
from .models import Region, Périmètre, Fichier_mansuelle

def tableau_regions(request):
    somme_attributs_par_region = {}

    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')

        if not mois or not annee:  # Vérifier si mois ou année est None
            return render(request, 'traitement_p1.html', {'mois': mois, 'annee': annee})

        regions = Region.objects.all()

        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, mois=mois, annee=annee)

            # Calculer les sommes des attributs pour chaque région
            somme_stock_ini = fichiers_par_region.aggregate(somme_stock_ini=Sum('stock_ini', default=0, output_field=FloatField()))['somme_stock_ini']
            somme_apport_consommation = fichiers_par_region.aggregate(somme_apport_consommation=Sum('Apport_consommation', default=0, output_field=FloatField()))['somme_apport_consommation']
            somme_produit = fichiers_par_region.aggregate(somme_produit=Sum('produit', default=0, output_field=FloatField()))['somme_produit']
            somme_consomme = fichiers_par_region.aggregate(somme_consomme=Sum('consomme', default=0, output_field=FloatField()))['somme_consomme']
            somme_preleve = fichiers_par_region.aggregate(somme_preleve=Sum('preleve', default=0, output_field=FloatField()))['somme_preleve']
            somme_pertes = fichiers_par_region.aggregate(somme_pertes=Sum('pertes', default=0, output_field=FloatField()))['somme_pertes']
            somme_expedie = fichiers_par_region.aggregate(somme_expedie=Sum('expedie', default=0, output_field=FloatField()))['somme_expedie']
            somme_laivraison = fichiers_par_region.aggregate(somme_laivraison=Sum('laivraison', default=0, output_field=FloatField()))['somme_laivraison']

            # Calculer somme_exp_trc
            somme_exp_trc = fichiers_par_region.aggregate(somme_exp_trc=Sum(F('expedie') / F('densite'), default=0, output_field=FloatField()))['somme_exp_trc']

            # Calculer somme_stock_final
            somme_stock_final = somme_produit - somme_preleve - somme_pertes - somme_expedie + somme_laivraison + somme_stock_ini - somme_apport_consommation

            # Formater les valeurs pour n'afficher qu'un nombre fixe de décimales
            somme_stock_ini = "{:.3f}".format(somme_stock_ini or 0)
            somme_apport_consommation = "{:.3f}".format(somme_apport_consommation or 0)
            somme_produit = "{:.3f}".format(somme_produit or 0)
            somme_consomme = "{:.3f}".format(somme_consomme or 0)
            somme_preleve = "{:.3f}".format(somme_preleve or 0)
            somme_pertes = "{:.3f}".format(somme_pertes or 0)
            somme_expedie = "{:.3f}".format(somme_expedie or 0)
            somme_laivraison = "{:.3f}".format(somme_laivraison or 0)
            somme_exp_trc = "{:.3f}".format(somme_exp_trc or 0)
            somme_stock_final = "{:.3f}".format(somme_stock_final or 0)

            # Ajouter les sommes des attributs à la région
            somme_attributs_par_region[region] = {
                'somme_stock_ini': somme_stock_ini,
                'somme_apport_consommation': somme_apport_consommation,
                'somme_produit': somme_produit,
                'somme_consomme': somme_consomme,
                'somme_preleve': somme_preleve,
                'somme_pertes': somme_pertes,
                'somme_expedie': somme_expedie,
                'somme_laivraison': somme_laivraison,
                'somme_exp_trc': somme_exp_trc,
                'somme_stock_final': somme_stock_final,
            }

    return render(request, 'traitement_p1.html', {'somme_attributs_par_region': somme_attributs_par_region, 'mois': mois, 'annee': annee})


#ca marche tres bien 
def generate_pdf(request):
    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
        
        if not mois or not annee:  # Vérification si mois ou année est None
            return render(request, 'traitement_p1.html', {'mois': mois, 'annee': annee})
        # Fetch data as in the generate_excel function
        somme_attributs_par_region = {}
        regions = Region.objects.all()

        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, mois=mois, annee=annee)

            # Calculate attributes for each region
            somme_perimetre_attributs = []
            for perimetre in perimetres:
                somme_stock_ini = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_stock_ini=Coalesce(Sum('stock_ini'), Value(0), output_field=FloatField()))['somme_stock_ini'])
                somme_apport_consommation = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_apport_consommation=Coalesce(Sum('Apport_consommation'), Value(0), output_field=FloatField()))['somme_apport_consommation'])
                somme_produit = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_produit=Coalesce(Sum('produit'), Value(0), output_field=FloatField()))['somme_produit'])
                somme_consomme = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_consomme=Coalesce(Sum('consomme'), Value(0), output_field=FloatField()))['somme_consomme'])
                somme_preleve = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_preleve=Coalesce(Sum('preleve'), Value(0), output_field=FloatField()))['somme_preleve'])
                somme_pertes = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_pertes=Coalesce(Sum('pertes'), Value(0), output_field=FloatField()))['somme_pertes'])
                somme_expedie = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_expedie=Coalesce(Sum('expedie'), Value(0), output_field=FloatField()))['somme_expedie'])
                somme_laivraison = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_laivraison=Coalesce(Sum('laivraison'), Value(0), output_field=FloatField()))['somme_laivraison'])
                somme_exp_trc = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_exp_trc=Coalesce(Sum(F('expedie') / F('densite')), Value(0), output_field=FloatField()))['somme_exp_trc'])

                somme_stock_final = "{:.3f}".format(float(somme_produit) - float(somme_preleve) - float(somme_pertes) - float(somme_expedie) + float(somme_laivraison) + float(somme_stock_ini) - float(somme_apport_consommation))

                somme_perimetre_attributs.append({
                    'nom': perimetre.nom,
                    'somme_stock_ini': somme_stock_ini,
                    'somme_apport_consommation': somme_apport_consommation,
                    'somme_produit': somme_produit,
                    'somme_consomme': somme_consomme,
                    'somme_preleve': somme_preleve,
                    'somme_pertes': somme_pertes,
                    'somme_expedie': somme_expedie,
                    'somme_laivraison': somme_laivraison,
                    'somme_exp_trc': somme_exp_trc,
                    'somme_stock_final': somme_stock_final
                })

            somme_attributs_par_region[region] = somme_perimetre_attributs

        # Create PDF response and document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="regions_summary.pdf"'
        doc = SimpleDocTemplate(response, pagesize=landscape(A4),  # Use A4 landscape for more space
                           leftMargin=0.1*cm, rightMargin=0.1*cm, 
                           topMargin=0.1*cm, bottomMargin=0.1*cm)

        # Define table headers
        headers = ['Région', 'Périmètre', 'Stock initial', 'Consommation I', 'Production', 'Prélévement CI',
                   'Prélévement CP', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition TRC en m3', 'Stock final']

        # Define larger column widths
        col_widths = [3.4 * cm, 3.7 * cm, 2 * cm,2.3 * cm,2 * cm, 2.5 * cm,2.5 * cm, 1.5 * cm, 3.1 * cm, 1.5 * cm, 3.1 * cm, 2 * cm]

        # Create a list to hold table data
        table_data = [headers]

        # Add data for each region and perimetre
        for region, perimetres in somme_attributs_par_region.items():
            for perimetre_data in perimetres:
                row_data = [region.nom, perimetre_data['nom']]
                for attribut in ['somme_stock_ini', 'somme_apport_consommation', 'somme_produit', 'somme_consomme', 'somme_preleve', 'somme_pertes', 'somme_expedie', 'somme_laivraison', 'somme_exp_trc', 'somme_stock_final']:
                    row_data.append(perimetre_data[attribut])
                table_data.append(row_data)

            # Add totals for the perimetres
            perimetre_totals = ['Total pour ' + region.nom, '', *[float("{:.3f}".format(sum(float(perimetre_data[attribut]) for perimetre_data in perimetres))) for attribut in ['somme_stock_ini', 'somme_apport_consommation', 'somme_produit', 'somme_consomme', 'somme_preleve', 'somme_pertes', 'somme_expedie', 'somme_laivraison', 'somme_exp_trc', 'somme_stock_final']]]
            table_data.append(perimetre_totals)

        # Create table
        table = Table(table_data, colWidths=col_widths)

        # Add style for table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.orange),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
             ('FONTSIZE', (0, 1), (-1, -1), 7),
              ('FONTSIZE', (0, 0), (-1, 0), 8),  # Smaller font size
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines
        ])

        table.setStyle(style)

        # Add table to document
        doc.build([table])

        return response

#ca marche tres bien 
def generate_excel(request):
    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
        
        if not mois or not annee:  # Vérification si mois ou année est None
            return render(request, 'traitement_p1.html', {'mois': mois, 'annee': annee})
        
        regions = Region.objects.all()

        # Créer un nouveau classeur Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Régions"

        # Définir les styles
        bold_font = Font(bold=True)
        center_alignment = Alignment(horizontal='center')
        orange_fill = PatternFill(start_color='FFA500', end_color='FFA500', fill_type='solid')
        black_border = Border(left=Side(style='thin', color='000000'),
                              right=Side(style='thin', color='000000'),
                              top=Side(style='thin', color='000000'),
                              bottom=Side(style='thin', color='000000'))

        # Écrire le mois et l'année au début du document
        ws['A1'] = 'Mois : ' + mois
        ws['A2'] = 'Année : ' + annee

        # Fusionner les cellules pour afficher le mois et l'année
        ws.merge_cells('A1:B1')
        ws.merge_cells('A2:B2')

        # Appliquer le style aux cellules du mois et de l'année
        ws['A1'].font = bold_font
        ws['A1'].alignment = center_alignment
        ws['A2'].font = bold_font
        ws['A2'].alignment = center_alignment

        # Ajouter les noms des attributs en première ligne
        headers = ['Région', 'Périmètre', 'Stock initial', 'Apport de consommation interne', 'Production', 'Consommation interne',
                   'Prélévement ou consommation autre périmétre', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition vers TRC en m3', 'Stock final']

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_num, value=header)
            cell.font = bold_font
            cell.alignment = center_alignment
            cell.fill = orange_fill

        row_num = 4  # Commencer à partir de la ligne 4

        # Écrire les données pour chaque région
        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, mois=mois, annee=annee)

            # Écrire les données pour chaque périmètre dans la région
            for perimetre in perimetres:
                attributs = [
                    region.nom,
                    perimetre.nom,
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_stock_ini=Coalesce(Sum('stock_ini'), Value(0), output_field=FloatField()))['somme_stock_ini'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_apport_consommation=Coalesce(Sum('Apport_consommation'), Value(0), output_field=FloatField()))['somme_apport_consommation'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_produit=Coalesce(Sum('produit'), Value(0), output_field=FloatField()))['somme_produit'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_consomme=Coalesce(Sum('consomme'), Value(0), output_field=FloatField()))['somme_consomme'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_preleve=Coalesce(Sum('preleve'), Value(0), output_field=FloatField()))['somme_preleve'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_pertes=Coalesce(Sum('pertes'), Value(0), output_field=FloatField()))['somme_pertes'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_expedie=Coalesce(Sum('expedie'), Value(0), output_field=FloatField()))['somme_expedie'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_laivraison=Coalesce(Sum('laivraison'), Value(0), output_field=FloatField()))['somme_laivraison'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_exp_trc=Coalesce(Sum(F('expedie') / F('densite')), Value(0), output_field=FloatField()))['somme_exp_trc'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_stock_final=Coalesce(Sum(F('produit') - F('preleve') - F('pertes') - F('expedie') + F('laivraison') + F('stock_ini') - F('Apport_consommation')), Value(0), output_field=FloatField()))['somme_stock_final']
                ]

                # Écrire les données avec style
                for col_num, value in enumerate(attributs, 1):
                    cell = ws.cell(row=row_num, column=col_num, value=value)
                    cell.alignment = center_alignment

                row_num += 1  # Déplacer vers la ligne suivante

            # Écrire le total des périmètres pour cette région
            total_attributs = []
            for col_num in range(3, ws.max_column + 1):
                total = sum(ws.cell(row=row, column=col_num).value or 0 for row in range(row_num - len(perimetres), row_num))
                total_attributs.append(total)

            # Écrire les totaux dans la même colonne que les attributs correspondants
            for col_num, value in enumerate(total_attributs, 3):
                cell = ws.cell(row=row_num, column=col_num, value=value)
                cell.font = bold_font
                cell.alignment = center_alignment

            # Écrire le texte "Total pour région" dans la première colonne
            cell = ws.cell(row=row_num, column=1, value="Total pour " + region.nom)
            cell.font = bold_font
            cell.alignment = center_alignment

            row_num += 1  # Déplacer vers la ligne suivante

        # Ajuster la largeur des colonnes
        for col_num in range(1, ws.max_column + 1):
            column_letter = get_column_letter(col_num)
            ws.column_dimensions[column_letter].auto_size = True

        # Appliquer les bordures à toutes les cellules
        for row in ws.iter_rows():
            for cell in row:
                cell.border = black_border

        # Générer le fichier Excel en mémoire
        excel_data = BytesIO()
        wb.save(excel_data)
        excel_data.seek(0)

        # Créer une réponse HTTP avec le fichier Excel
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=bilan_par_périmétre.xlsx'

        return response

def tableau_regions_annuel(request, annee=None):
    somme_attributs_par_region = {}
    
    if request.method == 'POST':
        annee = request.POST.get('annee')
    if not annee:  # Vérifier si l'année est None
            return render(request, 'traitement_annuel.html', {'annee': annee})
    if annee:
        regions = Region.objects.all()

        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, annee=annee)
            
            # Calculer les sommes des attributs pour chaque région
            somme_stock_ini = fichiers_par_region.aggregate(somme_stock_ini=Sum('stock_ini', default=0, output_field=FloatField()))['somme_stock_ini']
            somme_apport_consommation = fichiers_par_region.aggregate(somme_apport_consommation=Sum('Apport_consommation', default=0, output_field=FloatField()))['somme_apport_consommation']
            somme_produit = fichiers_par_region.aggregate(somme_produit=Sum('produit', default=0, output_field=FloatField()))['somme_produit']
            somme_consomme = fichiers_par_region.aggregate(somme_consomme=Sum('consomme', default=0, output_field=FloatField()))['somme_consomme']
            somme_preleve = fichiers_par_region.aggregate(somme_preleve=Sum('preleve', default=0, output_field=FloatField()))['somme_preleve']
            somme_pertes = fichiers_par_region.aggregate(somme_pertes=Sum('pertes', default=0, output_field=FloatField()))['somme_pertes']
            somme_expedie = fichiers_par_region.aggregate(somme_expedie=Sum('expedie', default=0, output_field=FloatField()))['somme_expedie']
            somme_laivraison = fichiers_par_region.aggregate(somme_laivraison=Sum('laivraison', default=0, output_field=FloatField()))['somme_laivraison']

            # Calculer somme_exp_trc
            somme_exp_trc = fichiers_par_region.aggregate(somme_exp_trc=Sum(F('expedie') / F('densite'), default=0, output_field=FloatField()))['somme_exp_trc']

            # Calculer somme_stock_final
            somme_stock_final = somme_produit - somme_preleve - somme_pertes - somme_expedie + somme_laivraison + somme_stock_ini - somme_apport_consommation
            
            # Formater les valeurs pour n'afficher qu'un nombre fixe de décimales
            somme_stock_ini = "{:.3f}".format(somme_stock_ini or 0)
            somme_apport_consommation = "{:.3f}".format(somme_apport_consommation or 0)
            somme_produit = "{:.3f}".format(somme_produit or 0)
            somme_consomme = "{:.3f}".format(somme_consomme or 0)
            somme_preleve = "{:.3f}".format(somme_preleve or 0)
            somme_pertes = "{:.3f}".format(somme_pertes or 0)
            somme_expedie = "{:.3f}".format(somme_expedie or 0)
            somme_laivraison = "{:.3f}".format(somme_laivraison or 0)
            somme_exp_trc = "{:.3f}".format(somme_exp_trc or 0)
            somme_stock_final = "{:.3f}".format(somme_stock_final or 0)
            
            # Ajouter les sommes des attributs à la région
            somme_attributs_par_region[region] = {
                'somme_stock_ini': somme_stock_ini,
                'somme_apport_consommation': somme_apport_consommation,
                'somme_produit': somme_produit,
                'somme_consomme': somme_consomme,
                'somme_preleve': somme_preleve,
                'somme_pertes': somme_pertes,
                'somme_expedie': somme_expedie,
                'somme_laivraison': somme_laivraison,
                'somme_exp_trc': somme_exp_trc,
                'somme_stock_final': somme_stock_final,
            }

    return render(request, 'traitement_annuel.html', {'somme_attributs_par_region': somme_attributs_par_region, 'annee': annee})


#ca marche
def generate_pdf_annuel(request):
    if request.method == 'POST':
        annee = request.POST.get('annee')

        if not annee:  # Vérifier si l'année est None
            return render(request, 'traitement_annuel.html', {'annee': annee})

        # Fetch data for the selected year
        somme_attributs_par_region = {}
        regions = Region.objects.all()

        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, annee=annee)
            
            # Calculate attribute sums for each region
            somme_perimetre_attributs = []
            for perimetre in perimetres:
                somme_stock_ini = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_stock_ini=Coalesce(Sum('stock_ini'), Value(0), output_field=FloatField()))['somme_stock_ini'])
                somme_apport_consommation = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_apport_consommation=Coalesce(Sum('Apport_consommation'), Value(0), output_field=FloatField()))['somme_apport_consommation'])
                somme_produit = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_produit=Coalesce(Sum('produit'), Value(0), output_field=FloatField()))['somme_produit'])
                somme_consomme = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_consomme=Coalesce(Sum('consomme'), Value(0), output_field=FloatField()))['somme_consomme'])
                somme_preleve = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_preleve=Coalesce(Sum('preleve'), Value(0), output_field=FloatField()))['somme_preleve'])
                somme_pertes = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_pertes=Coalesce(Sum('pertes'), Value(0), output_field=FloatField()))['somme_pertes'])
                somme_expedie = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_expedie=Coalesce(Sum('expedie'), Value(0), output_field=FloatField()))['somme_expedie'])
                somme_laivraison = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_laivraison=Coalesce(Sum('laivraison'), Value(0), output_field=FloatField()))['somme_laivraison'])
                somme_exp_trc = "{:.3f}".format(fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_exp_trc=Coalesce(Sum(F('expedie') / F('densite')), Value(0), output_field=FloatField()))['somme_exp_trc'])

                somme_stock_final = "{:.3f}".format(float(somme_produit) - float(somme_preleve) - float(somme_pertes) - float(somme_expedie) + float(somme_laivraison) + float(somme_stock_ini) - float(somme_apport_consommation))

                somme_perimetre_attributs.append({
                    'nom': perimetre.nom,
                    'somme_stock_ini': somme_stock_ini,
                    'somme_apport_consommation': somme_apport_consommation,
                    'somme_produit': somme_produit,
                    'somme_consomme': somme_consomme,
                    'somme_preleve': somme_preleve,
                    'somme_pertes': somme_pertes,
                    'somme_expedie': somme_expedie,
                    'somme_laivraison': somme_laivraison,
                    'somme_exp_trc': somme_exp_trc,
                    'somme_stock_final': somme_stock_final
                })

            somme_attributs_par_region[region] = somme_perimetre_attributs

             # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="regions_summary.pdf"'
        doc = SimpleDocTemplate(response, pagesize=landscape(A4),  # Use A4 landscape for more space
                           leftMargin=0.1*cm, rightMargin=0.1*cm, 
                           topMargin=0.1*cm, bottomMargin=0.1*cm)
        
        headers = ['Région', 'Périmètre', 'Stock initial', 'Consommation I', 'Production', 'Prélévement CI',
                   'Prélévement CP', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition TRC en m3', 'Stock final']

        # Define larger column widths
        col_widths = [3.4 * cm, 3.7 * cm, 2 * cm,2.3 * cm,2 * cm, 2.5 * cm,2.5 * cm, 1.5 * cm, 3.1 * cm, 1.5 * cm, 3.1 * cm, 2 * cm]

        # Create a list to hold table data
        table_data = [headers]

        # Add data for each region and perimetre
        for region, perimetres in somme_attributs_par_region.items():
            for perimetre_data in perimetres:
                row_data = [region.nom, perimetre_data['nom']]
                for attribut in ['somme_stock_ini', 'somme_apport_consommation', 'somme_produit', 'somme_consomme', 'somme_preleve', 'somme_pertes', 'somme_expedie', 'somme_laivraison', 'somme_exp_trc', 'somme_stock_final']:
                    row_data.append(perimetre_data[attribut])
                table_data.append(row_data)

            # Add totals for the perimetres
            perimetre_totals = ['Total pour ' + region.nom, '', *[float("{:.3f}".format(sum(float(perimetre_data[attribut]) for perimetre_data in perimetres))) for attribut in ['somme_stock_ini', 'somme_apport_consommation', 'somme_produit', 'somme_consomme', 'somme_preleve', 'somme_pertes', 'somme_expedie', 'somme_laivraison', 'somme_exp_trc', 'somme_stock_final']]]
            table_data.append(perimetre_totals)

        # Create table
        table = Table(table_data, colWidths=col_widths)

        # Add style for table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.orange),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('FONTSIZE', (0, 0), (-1, 0), 8),  # Smaller font size
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines
        ])

        table.setStyle(style)

        # Add table to document
        doc.build([table])

        table.setStyle(style)

        # Add table to document
        doc.build([table])

        return response


def generate_excel_annuele(request):
    if request.method == 'POST':
        annee = request.POST.get('annee')

        if not annee:  # Vérifier si l'année est None
            return render(request, 'traitement_annuel.html', {'annee': annee})

        regions = Region.objects.all()

        # Créer un nouveau classeur Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Régions"

        # Définir les styles
        bold_font = Font(bold=True)
        center_alignment = Alignment(horizontal='center')
        orange_fill = PatternFill(start_color='FFA500', end_color='FFA500', fill_type='solid')
        black_border = Border(left=Side(style='thin', color='000000'),
                              right=Side(style='thin', color='000000'),
                              top=Side(style='thin', color='000000'),
                              bottom=Side(style='thin', color='000000'))

        # Écrire le mois et l'année au début du document
        ws['A1'] = 'Année : ' + annee

        # Fusionner les cellules pour afficher le mois et l'année
        ws.merge_cells('A1:B1')

        # Appliquer le style aux cellules du mois et de l'année
        ws['A1'].font = bold_font
        ws['A1'].alignment = center_alignment

        # Ajouter les noms des attributs en première ligne
        headers = ['Région', 'Périmètre', 'Stock initial', 'Apport de consommation interne', 'Production', 'Consommation',
                   'Prélevé', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition vers TRC en m3', 'Stock final']

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_num, value=header)
            cell.font = bold_font
            cell.alignment = center_alignment
            cell.fill = orange_fill

        row_num = 4  # Commencer à partir de la ligne 4

        # Écrire les données pour chaque région
        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, annee=annee)

            # Écrire les données pour chaque périmètre dans la région
            for perimetre in perimetres:
                attributs = [
                    region.nom,
                    perimetre.nom,
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_stock_ini=Coalesce(Sum('stock_ini'), Value(0), output_field=FloatField()))['somme_stock_ini'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_apport_consommation=Coalesce(Sum('Apport_consommation'), Value(0), output_field=FloatField()))['somme_apport_consommation'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_produit=Coalesce(Sum('produit'), Value(0), output_field=FloatField()))['somme_produit'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_consomme=Coalesce(Sum('consomme'), Value(0), output_field=FloatField()))['somme_consomme'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_preleve=Coalesce(Sum('preleve'), Value(0), output_field=FloatField()))['somme_preleve'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_pertes=Coalesce(Sum('pertes'), Value(0), output_field=FloatField()))['somme_pertes'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_expedie=Coalesce(Sum('expedie'), Value(0), output_field=FloatField()))['somme_expedie'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_laivraison=Coalesce(Sum('laivraison'), Value(0), output_field=FloatField()))['somme_laivraison'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_exp_trc=Coalesce(Sum(F('expedie') / F('densite')), Value(0), output_field=FloatField()))['somme_exp_trc'],
                    fichiers_par_region.filter(périmètre=perimetre).aggregate(somme_stock_final=Coalesce(Sum(F('produit') - F('preleve') - F('pertes') - F('expedie') + F('laivraison') + F('stock_ini') - F('Apport_consommation')), Value(0), output_field=FloatField()))['somme_stock_final']
                ]

                # Écrire les données avec style
                for col_num, value in enumerate(attributs, 1):
                    cell = ws.cell(row=row_num, column=col_num, value=value)
                    cell.alignment = center_alignment

                row_num += 1  # Déplacer vers la ligne suivante

            # Écrire le total des périmètres pour cette région
            total_attributs = []
            for col_num in range(3, ws.max_column + 1):
                total = sum(ws.cell(row=row, column=col_num).value or 0 for row in range(row_num - len(perimetres), row_num))
                total_attributs.append(total)

            # Écrire les totaux dans la même colonne que les attributs correspondants
            for col_num, value in enumerate(total_attributs, 3):
                cell = ws.cell(row=row_num, column=col_num, value=value)
                cell.font = bold_font
                cell.alignment = center_alignment

            # Écrire le texte "Total pour région" dans la première colonne
            cell = ws.cell(row=row_num, column=1, value="Total pour " + region.nom)
            cell.font = bold_font
            cell.alignment = center_alignment

            row_num += 1  # Déplacer vers la ligne suivante

        # Ajuster la largeur des colonnes
        for col_num in range(1, ws.max_column + 1):
            column_letter = get_column_letter(col_num)
            ws.column_dimensions[column_letter].auto_size = True

        # Appliquer les bordures à toutes les cellules
        for row in ws.iter_rows():
            for cell in row:
                cell.border = black_border

        # Générer le fichier Excel en mémoire
        excel_data = BytesIO()
        wb.save(excel_data)
        excel_data.seek(0)

        # Créer une réponse HTTP avec le fichier Excel
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=bilan_annuel.xlsx'

        return response

from datetime import datetime
from django.db.models import Sum, Count
from .models import Fichier_mansuelle, Prévision_perimetre
from django.http import JsonResponse
from django.db.utils import IntegrityError

def extract_data_for_visualization(date_debut: str, date_fin: str, region: str) -> dict:
    """
    Extract data for visualization.

    Args:
    - date_debut (str): Start date in 'YYYY-MM-DD' format.
    - date_fin (str): End date in 'YYYY-MM-DD' format.
    - region (str): Region name.

    Returns:
    - dict: Data for visualization.
    """
    # Convert date strings to datetime objects
   
    date_format = "%m"  # adjust this format according to your data
    mois_francais = {
    'janvier': '01',
    'février': '02',
    'mars': '03',
    'avril': '04',
    'mai': '05',
    'juin': '06',
    'juillet': '07',
    'août': '08',
    'septembre': '09',
    'octobre': '10',
    'novembre': '11',
    'décembre': '12'
    }
    for fichier in Fichier_mansuelle.objects.all():
        if fichier.mois in mois_francais:
            fichier.mois = mois_francais[fichier.mois]
            try:
                fichier.save()
            except IntegrityError:
                pass
    date_debut = datetime.strptime(date_debut, "%Y-%m")
    date_fin = datetime.strptime(date_fin, "%Y-%m")
    print(date_debut.year)

# Filter fichiers
    fichiers = Fichier_mansuelle.objects.filter(
        Q(annee__gte=date_debut.year, mois__gte=date_debut.month) &
        Q(annee__lte=date_fin.year, mois__lte=date_fin.month) &
        Q(périmètre__region__nom=region)
    )
    

    # Calculate production sum for each perimeter
    production_par_perimetre = fichiers.values('périmètre__nom').annotate(production=Sum('produit'))

    # Calculate total production for the specified period
    total_production = fichiers.aggregate(total=Sum('produit'))['total'] or 0

    # Calculate percentages of production for each perimeter
    data_pie_chart = [
        {'perimetre': item['périmètre__nom'], 'percentage': (item['production'] / total_production) * 100 if total_production!= 0 else 0}
        for item in production_par_perimetre
    ]
    for data in data_pie_chart:
        data['percentage'] = float(data['percentage']) 
    

    # Calculate average production for each month
    moyenne_production_mensuelle = fichiers.values('mois','périmètre__nom').annotate(moyenne_production=Sum('produit') / Count('périmètre'))

    # Calculate predictions for each perimeter
    previsions = Prévision_perimetre.objects.filter(
        Q(annee__gte=date_debut.year, mois__gte=date_debut.month) &
        Q(annee__lte=date_fin.year, mois__lte=date_fin.month) &
        Q(périmètre__region__nom=region)

    )
    print(previsions)

    # Calculate real production and prediction for each month
    production_previsions = [
        {
           
            'perimetre': item['périmètre__nom'],
            'production_mensuelle': item['moyenne_production'],
            'prevision': previsions.filter(mois=item['mois']).aggregate(prevision=Sum('prévision'))['prevision'] or 0
        }
        for item in moyenne_production_mensuelle
    ]

    moyenne_production_mensuelle_mois = fichiers.values('mois').annotate(moyenne_production=Sum('produit') / Count('mois'))
    production_previsions_mois = [
        {
           
            'mois': item['mois'],
            'production_mensuelle': item['moyenne_production'],
            'prevision': previsions.filter(mois=item['mois']).aggregate(prevision=Sum('prévision'))['prevision'] or 0
        }
        for item in moyenne_production_mensuelle_mois
    ]


    for d in production_previsions:
        d['production_mensuelle'] = float(d['production_mensuelle']) 
        d['prevision'] = float(d['prevision']) 

    for d in production_previsions_mois:
        d['production_mensuelle'] = float(d['production_mensuelle']) 
        d['prevision'] = float(d['prevision']) 



    # return {'data_pie_chart': data_pie_chart, 'production_previsions': production_previsions, 'total':total_production}
    return {'data_pie_chart': data_pie_chart,'total':total_production,'production_previsions': production_previsions, 'production_previsions_mois': production_previsions_mois}

def get_chart_data(request):
    if request.method == 'POST':
        date_debut = request.POST.get('dateDebut')
        date_fin = request.POST.get('dateFin')
        region = request.POST.get('region')
    
        data = extract_data_for_visualization(date_debut, date_fin, region)

        context = {
        "data_pie_chart": data['data_pie_chart'],
        "total": data['total'],
        'productionPrev':data['production_previsions'],
        'production_previsions_mois':data['production_previsions_mois'],
        'dateDeb':date_debut,
        'dateFin':date_fin,
        'region':region
        }
        return render(request, 'dashboard.html',context=context)

    data = extract_data_for_visualization("2020-01", "2030-12", "Adrar")
    context = {
        "data_pie_chart": data['data_pie_chart'],
        "total": data['total'],
        'productionPrev':data['production_previsions'],
        'production_previsions_mois':data['production_previsions_mois']
        }
    return render(request, 'dashboard.html',context=context)

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from io import BytesIO
from .models import Region, Fichier_mansuelle, Prévision_perimetre
from django.db.models import Sum, Count, Q, Value, F, FloatField
from django.db.models.functions import Coalesce
from django.db.models import Case, When
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from io import BytesIO
from .models import Region, Fichier_mansuelle, Prévision_perimetre
from django.db.models import Sum, Count, Q, Value, F
from django.db.models import Case, When
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from io import BytesIO
from .models import Region, Fichier_mansuelle, Prévision_perimetre
from django.db.models import Sum, Count, Q, Value, F, FloatField
from django.db.models.functions import Coalesce
from django.db.models import Case, When
from datetime import datetime

def generate_excel_from_extract(request):
    if request.method == 'POST':
        date_debut_str = request.POST.get('dateDebut')
        date_fin_str = request.POST.get('dateFin')
        region_nom = request.POST.get('region')
        error_message = request.POST.get('error', '')

        try:
            date_debut = datetime.strptime(date_debut_str, "%Y-%m")
            date_fin = datetime.strptime(date_fin_str, "%Y-%m")
            region = Region.objects.get(nom=region_nom)
        except ValueError:
            error_message = "Format de date incorrect. Utilisez YYYY-MM."
        except Region.DoesNotExist:
            error_message = "Région introuvable."

        if error_message:
            request.POST._mutable = True
            request.POST['error'] = error_message
            return render(request, 'dashboard.html', request.POST)
        mois_francais = {
            'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
            'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
            'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
        }
        try:
        # Mise à jour des mois en français vers leur équivalent numérique
         Fichier_mansuelle.objects.filter(mois__in=mois_francais.keys()).update(
            mois=Case(
                *[When(mois=k, then=Value(v)) for k, v in mois_francais.items()],
                default=F('mois')
            )
         )
        except IntegrityError:
         pass

        fichiers = Fichier_mansuelle.objects.filter(
            Q(annee__gte=date_debut.year, mois__gte=date_debut.month) &
            Q(annee__lte=date_fin.year, mois__lte=date_fin.month) &
            Q(périmètre__region=region)
        )

        production_par_perimetre = fichiers.values('périmètre__nom').annotate(production=Sum('produit'))
        total_production = fichiers.aggregate(total=Sum('produit'))['total'] or 0

        moyenne_production_mensuelle = fichiers.values('mois', 'périmètre__nom').annotate(moyenne_production=Sum('produit') / Count('périmètre'))

        previsions = Prévision_perimetre.objects.filter(
            Q(annee__gte=date_debut.year, mois__gte=date_debut.month) &
            Q(annee__lte=date_fin.year, mois__lte=date_fin.month) &
            Q(périmètre__region=region)
        )

        production_previsions = [
            {
                'perimetre': item['périmètre__nom'],
                'production_mensuelle': item['moyenne_production'],
                'prevision': previsions.filter(mois=item['mois']).aggregate(prevision=Sum('prévision'))['prevision'] or 0
            }
            for item in moyenne_production_mensuelle
        ]

        # --- Création du fichier Excel ---
        wb = Workbook()
        ws = wb.active
        ws.title = f"Données de {region_nom}"

        # Styles
        bold_font = Font(bold=True)
        center_alignment = Alignment(horizontal='center')
        orange_fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        # Date et région en première ligne
        ws.merge_cells('A1:C1')
        ws['A1'] = f"Région: {region_nom} - Période: {date_debut_str} à {date_fin_str}"
        ws['A1'].font = bold_font
        ws['A1'].alignment = center_alignment

        # En-têtes
        headers = ['Périmètre', 'Production', 'Prévision']
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_num, value=header)  # Ligne 3 pour les en-têtes
            cell.font = bold_font
            cell.alignment = center_alignment
            cell.fill = orange_fill
            cell.border = thin_border

        # Écriture des données
        row_num = 4  # Commencer à la ligne 4 (après les en-têtes)
        for data in production_previsions:
            ws.cell(row=row_num, column=1, value=data['perimetre']).border = thin_border
            ws.cell(row=row_num, column=2, value=data['production_mensuelle']).border = thin_border
            ws.cell(row=row_num, column=3, value=data['prevision']).border = thin_border
            row_num += 1

        # Total (ligne après les données)
        ws.cell(row=row_num, column=1, value="Total").font = bold_font
        ws.cell(row=row_num, column=1).border = thin_border
        ws.cell(row=row_num, column=2, value=total_production).font = bold_font
        ws.cell(row=row_num, column=2).border = thin_border

        # Ajustement des colonnes
        for col_idx in range(1, ws.max_column + 1):  # Itérer sur les indices de colonnes
           max_length = 0
           column_letter = get_column_letter(col_idx)  # Obtenir la lettre de la colonne à partir de l'index

           for row_idx in range(1, ws.max_row + 1):  # Itérer sur les indices de lignes
             cell = ws.cell(row=row_idx, column=col_idx)
             if cell.value:
                max_length = max(max_length, len(str(cell.value)))
    
             adjusted_width = max_length + 2  # padding
             ws.column_dimensions[column_letter].width = adjusted_width

        # Générer le fichier Excel
        excel_data = BytesIO()
        wb.save(excel_data)
        excel_data.seek(0)

        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=donnees_{region_nom}_{date_debut_str}_{date_fin_str}.xlsx'

        return response
