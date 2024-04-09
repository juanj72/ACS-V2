from django.urls import path

from cliente.api.views import ClienteCreateView, ClientesListView, ClienteView

urlpatterns = [
    path("clientes", ClientesListView.as_view()),
    path("cliente/create", ClienteCreateView.as_view()),
    path("cliente/<int:cliente_id>", ClienteView.as_view()),
]
