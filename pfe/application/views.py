from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Fichier_mansuelle , Périmètre
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)

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
def login(request):
   return render(request,'page-login.html')
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
    

