from django.http import HttpResponse,HttpResponseBadRequest
import pandas as pd
from .models import Fichier_mansuelle , Périmètre
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur, Fichier_mansuelle ,Périmètre,Region
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from django.db import models

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
def traitement_p1(request):
   return render(request,'traitement_p1.html')
def traitement_annuel(request):
   return render(request,'traitement_annuel.html')


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

"""
juste aussi
def tableau_regions(request, mois=None, annee=None):
    somme_attributs_par_region = {}
    
    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
    
    if mois and annee:
        regions = Region.objects.all()

        for region in regions:
            # Obtenir les périmètres de cette région
            perimetres = Périmètre.objects.filter(region=region)
            
            # Obtenir tous les fichiers pour ces périmètres pour le mois et l'année spécifiés
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, mois=mois, annee=annee)
            
            # Calculer la somme des attributs pour chaque région
            somme_stock_ini = fichiers_par_region.aggregate(somme_stock_ini=Sum('stock_ini'))['somme_stock_ini'] or 0
            somme_apport_consommation = fichiers_par_region.aggregate(somme_apport_consommation=Sum('Apport_consommation'))['somme_apport_consommation'] or 0
            somme_produit = fichiers_par_region.aggregate(somme_produit=Sum('produit'))['somme_produit'] or 0
            somme_consomme = fichiers_par_region.aggregate(somme_consomme=Sum('consomme'))['somme_consomme'] or 0
            somme_preleve = fichiers_par_region.aggregate(somme_preleve=Sum('preleve'))['somme_preleve'] or 0
            somme_pertes = fichiers_par_region.aggregate(somme_pertes=Sum('pertes'))['somme_pertes'] or 0
            somme_expedie = fichiers_par_region.aggregate(somme_expedie=Sum('expedie'))['somme_expedie'] or 0
            somme_laivraison = fichiers_par_region.aggregate(somme_laivraison=Sum('laivraison'))['somme_laivraison'] or 0

            # Calcul des nouvelles colonnes
            somme_exp_trc = fichiers_par_region.aggregate(somme_exp_trc=Sum(F('expedie') / F('densite')))['somme_exp_trc'] or 0
            somme_stock_final = somme_produit - somme_preleve - somme_pertes - somme_expedie + somme_laivraison + somme_stock_ini - somme_apport_consommation

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

    return render(request, 'traitement_p1.html', {'somme_attributs_par_region': somme_attributs_par_region, 'mois': mois})
   """
#justee****************
def tableau_regions(request, mois=None, annee=None):
    somme_attributs_par_region = {}
    
    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
    
    if mois and annee:
        regions = Region.objects.all()

        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, mois=mois, annee=annee)
            
            # Calculer les sommes des attributs pour chaque région
            somme_stock_ini = fichiers_par_region.aggregate(somme_stock_ini=Coalesce(Sum('stock_ini'), 0, output_field=FloatField()))['somme_stock_ini']
            somme_apport_consommation = fichiers_par_region.aggregate(somme_apport_consommation=Coalesce(Sum('Apport_consommation'), 0, output_field=FloatField()))['somme_apport_consommation']
            somme_produit = fichiers_par_region.aggregate(somme_produit=Coalesce(Sum('produit'), 0, output_field=FloatField()))['somme_produit']
            somme_consomme = fichiers_par_region.aggregate(somme_consomme=Coalesce(Sum('consomme'), 0, output_field=FloatField()))['somme_consomme']
            somme_preleve = fichiers_par_region.aggregate(somme_preleve=Coalesce(Sum('preleve'), 0, output_field=FloatField()))['somme_preleve']
            somme_pertes = fichiers_par_region.aggregate(somme_pertes=Coalesce(Sum('pertes'), 0, output_field=FloatField()))['somme_pertes']
            somme_expedie = fichiers_par_region.aggregate(somme_expedie=Coalesce(Sum('expedie'), 0, output_field=FloatField()))['somme_expedie']
            somme_laivraison = fichiers_par_region.aggregate(somme_laivraison=Coalesce(Sum('laivraison'), 0, output_field=FloatField()))['somme_laivraison']

            # Calculer somme_exp_trc avec Coalesce
            somme_exp_trc = fichiers_par_region.aggregate(somme_exp_trc=Coalesce(Sum(F('expedie') / F('densite')), 0, output_field=FloatField()))['somme_exp_trc']

            # Calculer somme_stock_final
            somme_stock_final = somme_produit - somme_preleve - somme_pertes - somme_expedie + somme_laivraison + somme_stock_ini - somme_apport_consommation
            
            # Formater les valeurs pour n'afficher qu'un nombre fixe de décimales
            somme_stock_ini = "{:.3f}".format(somme_stock_ini)
            somme_apport_consommation = "{:.3f}".format(somme_apport_consommation)
            somme_produit = "{:.3f}".format(somme_produit)
            somme_consomme = "{:.3f}".format(somme_consomme)
            somme_preleve = "{:.3f}".format(somme_preleve)
            somme_pertes = "{:.3f}".format(somme_pertes)
            somme_expedie = "{:.3f}".format(somme_expedie)
            somme_laivraison = "{:.3f}".format(somme_laivraison)
            somme_exp_trc = "{:.3f}".format(somme_exp_trc)
            somme_stock_final = "{:.3f}".format(somme_stock_final)
            
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

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce
from .models import Region, Périmètre, Fichier_mansuelle

def generate_pdf(request):
    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')

        # Fetch data as in the tableau_regions view
        somme_attributs_par_region = {}
        regions = Region.objects.all()

        for region in regions:
            perimetres = Périmètre.objects.filter(region=region)
            fichiers_par_region = Fichier_mansuelle.objects.filter(périmètre__in=perimetres, mois=mois, annee=annee)

            # Calculate attributes for each region
            somme_stock_ini = fichiers_par_region.aggregate(somme_stock_ini=Coalesce(Sum('stock_ini'), 0, output_field=FloatField()))['somme_stock_ini']
            somme_apport_consommation = fichiers_par_region.aggregate(somme_apport_consommation=Coalesce(Sum('Apport_consommation'), 0, output_field=FloatField()))['somme_apport_consommation']
            somme_produit = fichiers_par_region.aggregate(somme_produit=Coalesce(Sum('produit'), 0, output_field=FloatField()))['somme_produit']
            somme_consomme = fichiers_par_region.aggregate(somme_consomme=Coalesce(Sum('consomme'), 0, output_field=FloatField()))['somme_consomme']
            somme_preleve = fichiers_par_region.aggregate(somme_preleve=Coalesce(Sum('preleve'), 0, output_field=FloatField()))['somme_preleve']
            somme_pertes = fichiers_par_region.aggregate(somme_pertes=Coalesce(Sum('pertes'), 0, output_field=FloatField()))['somme_pertes']
            somme_expedie = fichiers_par_region.aggregate(somme_expedie=Coalesce(Sum('expedie'), 0, output_field=FloatField()))['somme_expedie']
            somme_laivraison = fichiers_par_region.aggregate(somme_laivraison=Coalesce(Sum('laivraison'), 0, output_field=FloatField()))['somme_laivraison']
            somme_exp_trc = fichiers_par_region.aggregate(somme_exp_trc=Coalesce(Sum(F('expedie') / F('densite')), 0, output_field=FloatField()))['somme_exp_trc']
            somme_stock_final = somme_produit - somme_preleve - somme_pertes - somme_expedie + somme_laivraison + somme_stock_ini - somme_apport_consommation

            # Format values to display only a fixed number of decimals
            somme_stock_ini = "{:.3f}".format(somme_stock_ini)
            somme_apport_consommation = "{:.3f}".format(somme_apport_consommation)
            somme_produit = "{:.3f}".format(somme_produit)
            somme_consomme = "{:.3f}".format(somme_consomme)
            somme_preleve = "{:.3f}".format(somme_preleve)
            somme_pertes = "{:.3f}".format(somme_pertes)
            somme_expedie = "{:.3f}".format(somme_expedie)

            # Store attributes for each region
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
                'somme_stock_final': somme_stock_final
            }

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="regions_summary.pdf"'

        # Create PDF document with landscape orientation
        #doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        doc = SimpleDocTemplate(response, pagesize=landscape(letter), leftMargin=1*cm, rightMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
        # Define table headers
        headers = ['Région', 'Stock initial', 'Apport de consommation interne', 'Production', 'Consommation',
                   'Prélevé', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition vers TRC en m3', 'Stock final']

        # Define larger column widths
        col_widths = [3.5 * cm, 2 * cm, 4 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2 * cm, 2.5 * cm, 2 * cm, 3 * cm, 3 * cm]

        # Create a table with the data and larger column widths
        table_data = [[region.nom, attributs['somme_stock_ini'], attributs['somme_apport_consommation'], attributs['somme_produit'],
                       attributs['somme_consomme'], attributs['somme_preleve'], attributs['somme_pertes'], attributs['somme_expedie'],
                       attributs['somme_laivraison'], attributs['somme_exp_trc'], "{:.3f}".format(attributs['somme_stock_final'])] for region, attributs in somme_attributs_par_region.items()]

        table = Table([headers] + table_data, colWidths=col_widths)

        # Apply table styles with smaller font size
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(1, 0.65, 0)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),  # Smaller font size
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Add the table to the PDF document
        doc.build([table])

        return response