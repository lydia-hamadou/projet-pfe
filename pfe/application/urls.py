from django.urls import path,include
from .views import essay1,essay2,essay3,essay4,essay5,login,essay7,upload_and_test_data

app_name = 'application'

urlpatterns = [
     path('upload-and-test/', upload_and_test_data, name='upload_and_test_data'),
    path('acceuil', essay1, name='acceuil'),
    path('traitement_mansuel', essay2, name='traitement_mansuel'),
    path('affichage_resutat_valide', essay3, name='affichage_resutat_valide'),
    path('affichage_resutat_nonvalide', essay4, name='affichage_resutat_nonvalide'),
    path('dashboard', essay5, name='dashboard'),
    path('compte', essay7, name='compte'),
    path('login',login, name='login'),
    path('', login, name='default_login')
]