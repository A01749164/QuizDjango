from django.urls import path
from .views import inicio, registro

# Jeovani Hernandez 
urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', registro, name='registro'),   
]
