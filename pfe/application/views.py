from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Fichier_mansuelle,Périmètre



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


def upload_file(request):
    error_message = None

    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            if uploaded_file.name.endswith('.xlsx'):
                try:
                    data = pd.read_excel(uploaded_file, engine='openpyxl')
                    data_list = data.to_dict('records')
                    # Further processing of data (optional)
                    # You might want to save the data to your models (Fichier_mansuelle, Périmètre)
                    # based on your specific requirements.
                    return render(request, 'affichage_Trait_mansuel.html', {'data': data_list})
                except (FileNotFoundError, pd.errors.ParserError) as e:
                    error_message = f"Error reading Excel file: {str(e)}"
            else:
                error_message = 'Invalid file type. Please upload an Excel file.'
        else:
            error_message = 'No file uploaded.'

    return render(request, 'Traitement_mansuel.html', {'error_message': error_message})

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
    

def test_data(request):
    if request.method == 'POST':
        data_list = request.POST.getlist('data')
        total = 0
        for row in data_list:
            stock_initial = row['stock_ini']
            apport_consommation = row['Apport_consommation']
            production = row['produit']
            prelevement_consommation = row['consomme'] + row['preleve']
            perte = row['pertes']
            expedition = row['expedie']
            livraison = row['laivraison']
            stock_final = stock_initial + apport_consommation + production - prelevement_consommation - perte - expedition - livraison
            if stock_final != 0:
                return render(request, 'test_results.html', {'error_message': f'Error: equation does not hold for row {data_list.index(row) + 1}. The formula is (stock_initial + apport_consommation + production - prelevement_consommation - perte - expedition - livraison - stock_final = 0), but the calculated stock_final is {stock_final}.'})
            total += stock_final
        return render(request, 'test_results.html', {'total': total})


    else:
        return HttpResponse('Invalid file type. Please upload an Excel file.')