from django.urls import path,include
from .views import essay1,essay2,essay3,essay4

app_name = 'application'

urlpatterns = [
    path('page1', essay1, name='achat_list'),
    path('page2', essay2, name='achat_list'),
    path('page3', essay3, name='achat_list'),
    path('page4', essay4, name='achat_list'),

]