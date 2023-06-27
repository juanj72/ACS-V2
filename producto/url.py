from django.urls import path,include
from producto.views import *

urlpatterns = [
    path('listado/',productos,name='productos'),
 
]