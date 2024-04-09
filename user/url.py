from django.urls import path

from user.views import confirmacionventa, index

urlpatterns = [
    path("", index, name="inicio"),
    path("confirmacion/<id>", confirmacionventa, name="okventa"),
]
