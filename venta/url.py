from django.urls import path
from venta.views import *
urlpatterns = [
    path('seleccion/',venta,name='seleccion'),
    path('recibo/<int:client>',crearrecibo,name='crearrecibo'),
    path('detalle/<reb>',detalleventa,name='detalle'),
    path('eliminar/<id>/<reb>',eliminardetail,name='eliminardetalle'),
    path('cerrar/<id>',cerrarrecibo,name='cerrarRecibo'),
    path('anular/<id>',anular,name = 'anular'),
    path('recibo_detalle/<id>',detalle_recibo,name='detalle_recibo'),
    path('listar/',listar,name='verventas')
]
 
