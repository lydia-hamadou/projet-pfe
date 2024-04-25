from django.urls import path
from .views import essay1,essay2,essay3,essay4,essay5,essay7,upload_and_test_data,login,essay6

app_name = 'application'

urlpatterns = [
    path('', essay6, name='app'),
    path('login/',login, name='login'),
    path('upload-and-test/', upload_and_test_data, name='upload_and_test_data'),
    path('login/acceuil', essay1, name='acceuil'),
    path('login/traitement_mansuel', essay2, name='traitement_mansuel'),
    path('affichage_resutat_valide', essay3, name='affichage_resutat_valide'),
    path('affichage_resutat_nonvalide', essay4, name='affichage_resutat_nonvalide'),
    path('dashboard', essay5, name='dashboard'),
    path('compte', essay7, name='compte'),
]