from django.urls import path,include
from .views import essay1,essay2,essay3,essay4,essay5,essay6,essay7,upload_file

app_name = 'application'

urlpatterns = [
    path('acceuil', essay1, name='acceuil'),
    path('traitement_mansuel', essay2, name='traitement_mansuel'),
    path('affichage_resutat_valide', essay3, name='affichage_resutat_valide'),
    path('affichage_resutat_nonvalide', essay4, name='affichage_resutat_nonvalide'),
    path('dashboard', essay5, name='dashboard'),
    path('login', essay6, name='login'),
    path('compte', essay7, name='compte'),
    path('upload_file/', upload_file, name='upload_file'),
]