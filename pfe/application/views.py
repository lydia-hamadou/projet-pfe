from django.http import HttpResponse
import pandas as pd
from .models import Fichier_mansuelle , Périmètre
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Utilisateur, Fichier_mansuelle ,Périmètre,Region
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
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Sum, F, Value, FloatField
from django.db.models.functions import Coalesce
from openpyxl.utils import get_column_letter
from openpyxl.styles.borders import Border, Side
from django.db.models import Q






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

            return render(request, 'page_fichier_sauvgarder.html')
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
from django.db.models import Sum, F, FloatField

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
        doc = SimpleDocTemplate(response, pagesize=landscape(letter), leftMargin=1*cm, rightMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)

        # Define table headers
        headers = ['Région', 'Périmètre', 'Stock initial', 'Apport pour Consommation interne', 'Production', 'Consommation interne',
                   'Prélévement pour la consommation autres périmétres', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition TRC en m3', 'Stock final']

        # Define larger column widths
        col_widths = [3.5 * cm, 3.5 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm]

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
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
             ('FONTSIZE', (0, 1), (-1, -1), 7),
              ('FONTSIZE', (0, 0), (-1, 0), 6),  # Smaller font size
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
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter), leftMargin=1*cm, rightMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)

        # Define table headers
        headers = ['Région', 'Périmètre', 'Stock initial', 'Apport de consommation interne', 'Production', 'Consommation',
                   'Prélevé', 'Pertes', 'Expédition vers TRC', 'Livraison', 'Expédition vers TRC en m3', 'Stock final']

        # Define larger column widths
        col_widths = [3.5 * cm, 3.5 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm]

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
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
             ('FONTSIZE', (0, 1), (-1, -1), 7),
              ('FONTSIZE', (0, 0), (-1, 0), 6),  # Smaller font size
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines
        ])

        table.setStyle(style)

        # Add table to document
        doc.build([table])

        # Set up response
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="regions_summary.pdf"'
        return response

def generate_excel_annuele(request):
    if request.method == 'POST':
        annee = request.POST.get('annee')

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
