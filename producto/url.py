from django.urls import path,include
from producto.views import *

urlpatterns = [
    path('listado/',productos,name='productos'),
    path('categorias/',categorias,name='categorias'),
    path('addcantidad/<pro>',addcantidadpro,name='addcantidad'),
    path('editar/<id>',editar_producto,name='editar_producto'),
    path('editar_categoria/<id>',editar_categoría,name='editar_categoría'),
    path('reportes/',reportes,name='reportes'),
    path('reporte_detalle/',detalle_reporte,name='detalle_reporte')
 
]