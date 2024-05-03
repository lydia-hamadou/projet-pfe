from django.urls import path
from .views import essay1,essay2,essay3,essay4,index,login,essay6,essay8,save_data,traitement_annuel,traitement_p1,tableau_regions,generate_pdf,generate_excel,tableau_regions_annuel,generate_pdf_annuel,generate_excel_annuele,dashboard,dashboard
                    

app_name = 'application'

urlpatterns = [
    path('', essay6, name='app'),
    path('login/',login, name='login'),
    path('index',index, name='index'),
    path('index/traitement_mansuel',essay2, name='allez'),
    path('save_data', save_data, name='save_data'),
    path('generate_pdf', generate_pdf, name='generate_pdf'),
    path('generate_excel', generate_excel, name='generate_excel'),
    path('tableau_regions', tableau_regions, name='tableau_regions'),
    path('tableau_regions_annuel', tableau_regions_annuel, name='tableau_regions_annuel'),
    path('generate_pdf_annuel', generate_pdf_annuel, name='generate_pdf_annuel'),
    path('generate_excel_annuele', generate_excel_annuele, name='generate_excel_annuele'),
    path('sauvgarder', essay8, name='sauvgarder'),
    path('login/acceuil', essay1, name='acceuil'),
     path('acceuil', essay1, name='acceuil'),
    path('login/traitement_mansuel', essay2, name='traitement_mansuel'),
    path('traitement_mansuel', essay2, name='traitement_mansuel'),
    path('affichage_resutat_valide', essay3, name='affichage_resutat_valide'),
    path('affichage_resutat_nonvalide', essay4, name='affichage_resutat_nonvalide'),
    path('login/traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('login/traitement_p1',traitement_p1, name='traitement_p1'),
    path('traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('traitement_p1',traitement_p1, name='traitement_p1'),
    path('login/dashboard',dashboard, name='dashboard'),
    path('dashboard',dashboard, name='dashboard'),
]