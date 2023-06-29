
from django.urls import path
from cliente.views import *

urlpatterns = [
    path('listado/',clientes,name='clientes'),
    path('crear/',crearCliente,name='crearCliente'),
    path('ventaAsignar/',asignarClienteVenta,name='asignarVenta')

]
