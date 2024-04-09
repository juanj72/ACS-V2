from django.urls import path

from venta.api.views import CerrarReciboView, DetalleVentaListView, ReciboCreateView

urlpatterns = [
    path("recibo/create/<int:cliente_id>", ReciboCreateView.as_view()),
    path("recibo/<int:recibo_id>/detalle-venta", DetalleVentaListView.as_view()),
    path("recibo/cerrar/<int:recibo_id>", CerrarReciboView.as_view()),
    # path('seleccion/',venta,name='seleccion'),
    # path('recibo/<int:client>',crearrecibo,name='crearrecibo'),
    # path('detalle/<reb>',detalleventa,name='detalle'),
    # path('eliminar/<id>/<reb>',eliminardetail,name='eliminardetalle'),
    # path('cerrar/<id>',cerrarrecibo,name='cerrarRecibo'),
    # path('anular/<id>',anular,name = 'anular'),
    # path('recibo_detalle/<id>',detalle_recibo,name='detalle_recibo'),
    # path('listar/',listar,name='verventas')
]
