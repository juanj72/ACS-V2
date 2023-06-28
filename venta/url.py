from django.urls import path
from venta.views import *
urlpatterns = [
    path('seleccion/',venta,name='seleccion'),
]
 
