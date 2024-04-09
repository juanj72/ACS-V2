from django.urls import path

from producto.api.views import (
    CategoriaCreateView,
    CategoriaListView,
    CategoriaView,
    ProductoAddCantidadView,
    ProductoCreateView,
    ProductoListView,
    ProductoView,
    ReportesView,
)

urlpatterns = [
    path("productos", ProductoListView.as_view(), name="productos"),
    path("producto/<int:producto_id>", ProductoView.as_view(), name="producto-update"),
    path("categorias", CategoriaListView.as_view(), name="categorias"),
    path("categoria/<int:categoria_id>", CategoriaView.as_view(), name="categoria-update"),
    path("producto/create", ProductoCreateView.as_view(), name="producto-create"),
    path("categoria/create", CategoriaCreateView.as_view(), name="categoria-create"),
    path("producto/<int:producto_id>/add_stock", ProductoAddCantidadView.as_view(), name="producto-add-stock"),
    path("reportes", ReportesView.as_view(), name="reportes"),
]
