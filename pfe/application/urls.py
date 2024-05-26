from django.urls import path
from .views import acceuil,taritemnt_mansuel,essay3,essay4,index,generate_excel_from_extract,get_chart_data,page_reponce,login,essay6,page_resultat_verifier,essay8,save_data,traitement_annuel,traitement_p1,tableau_regions,generate_pdf,generate_excel,tableau_regions_annuel,generate_pdf_annuel,generate_excel_annuele,dashboard,dashboard
                    

app_name = 'application'

urlpatterns = [
    path('', essay6, name='app'),
    path('login/',login, name='login'),
    path('save_data/login',login, name='login'),
    path('page_resultat_non_verifier/login',login, name='login'),
    path('tableau_regions/login',login, name='login'),
    path('page_resultat_verifier/login',login, name='login'),
    path('tableau_regions_annuel/login',login, name='login'),
    path('get_chart_data/login',login, name='login'),




    path('index',index, name='index'),
    path('generate_pdf', generate_pdf, name='generate_pdf'),
    path('generate_excel', generate_excel, name='generate_excel'),
    path('tableau_regions', tableau_regions, name='tableau_regions'),
    path('tableau_regions_annuel', tableau_regions_annuel, name='tableau_regions_annuel'),
    path('generate_pdf_annuel', generate_pdf_annuel, name='generate_pdf_annuel'),
    path('generate_excel_annuele', generate_excel_annuele, name='generate_excel_annuele'),
    path('sauvgarder', essay8, name='sauvgarder'),
    path('login/acceuil', acceuil, name='acceuil'),
    path('acceuil/login', acceuil, name='acceuil'),
    path('acceuil', acceuil, name='acceuil1'),
    path('save_data/acceuil', acceuil, name='acceuil'),
    path('page_resultat_non_verifier/acceuil',acceuil, name='acceuil'),
    path('page_resultat_verifier/acceuil',acceuil, name='acceuil'),


    path('save_data/traitement_mansuel',taritemnt_mansuel, name='traitement_mansuel'),
    path('save_data/traitement_p1',traitement_p1, name='traitement_p1'),
    path('save_data/traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('save_data/dashboard',dashboard, name='dashboard'),


    path('page_resultat_verifier/traitement_mansuel', taritemnt_mansuel, name='traitement_mansuel'),
    path('page_resultat_verifier/traitement_p1', traitement_p1, name='traitement_p1'),
    path('page_resultat_verifier/traitement_annuel', traitement_annuel, name='traitement_annuel'),
    path('page_resultat_verifier/dashboard', dashboard, name='dashboard'),

    path('page_resultat_non_verifier/traitement_mansuel',taritemnt_mansuel, name='traitement_mansuel'),
    path('page_resultat_non_verifier/traitement_p1',traitement_p1, name='traitement_p1'),
    path('page_resultat_non_verifier/traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('page_resultat_non_verifier/dashboard',dashboard, name='dashboard'),
    path('page_resultat_non_verifier/traitement_mansuel',taritemnt_mansuel, name='traitement_mansuel'),

    path('login/traitement_mansuel', taritemnt_mansuel, name='traitement_mansuel'),
    path('traitement_mansuel', taritemnt_mansuel, name='traitement_mansuel'),
    path('affichage_resutat_valide', essay3, name='affichage_resutat_valide'),
    path('affichage_resutat_nonvalide', essay4, name='affichage_resutat_nonvalide'),
    path('login/traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('login/traitement_p1',traitement_p1, name='traitement_p1'),
    path('traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('traitement_p1',traitement_p1, name='traitement_p1'),
    path('login/dashboard',dashboard, name='dashboard'),
    path('get_chart_data/dashboard',get_chart_data, name='dashboard2'),
    path('dashboard',get_chart_data, name='dashboard'),
    path('get_chart_data/', get_chart_data, name='get_chart_data'),
    path('save_data/', save_data, name='save_data'),
    path('page_resultat_verifier/', page_resultat_verifier, name='page_resultat_verifier'),
    path('page_reponce/', page_reponce, name='page_reponce'),
    path('generate_excel_from_extract/', generate_excel_from_extract, name='generate_excel_from_extract'),
    path('get_chart_data/acceuil', acceuil, name='acceuil'),
    
    path('get_chart_data/acceuil',acceuil, name='acceuil'),
    path('get_chart_data/traitement_mansuel',taritemnt_mansuel, name='traitement_mansuel'),
    path('get_chart_data/traitement_p1',traitement_p1, name='traitement_p1'),
    path('get_chart_data/traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('get_chart_data/dashboard',dashboard, name='dashboard'),
    
]