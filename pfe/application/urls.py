from django.urls import path
from .views import essay1,essay2,essay3,essay4,index,login,essay6,essay8,save_data,traitement_annuel,traitement_p1,tableau_regions

app_name = 'application'

urlpatterns = [
    path('', essay6, name='app'),
    path('login/',login, name='login'),
    path('index',index, name='index'),
    path('save_data', save_data, name='save_data'),
    path('tableau_regions', tableau_regions, name='tableau_regions'),
    path('sauvgarder', essay8, name='sauvgarder'),
    path('login/acceuil', essay1, name='acceuil'),
    path('login/traitement_mansuel', essay2, name='traitement_mansuel'),
    path('affichage_resutat_valide', essay3, name='affichage_resutat_valide'),
    path('affichage_resutat_nonvalide', essay4, name='affichage_resutat_nonvalide'),
    path('login/traitement_annuel',traitement_annuel, name='traitement_annuel'),
    path('login/traitement_p1',traitement_p1, name='traitement_p1'),
]