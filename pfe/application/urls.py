from django.urls import path,include
from .views import essay1,essay2,essay3,essay4,essay5,essay6

app_name = 'application'

urlpatterns = [
    path('acceuil', essay1, name='acceuil'),
    path('traitement_mansuel', essay2, name='traitement_mansuel'),
    path('traitement_p1', essay3, name='traitement_p1'),
    path('traitement_annuel', essay4, name='traitement_annuel'),
    path('dashboard', essay5, name='dashboard'),
    path('login', essay6, name='login'),
]