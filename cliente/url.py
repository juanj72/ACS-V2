
from django.urls import path
from cliente.views import *

urlpatterns = [
    path('listado/',clientes,name='clientes'),

]
