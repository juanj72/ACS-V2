from django.shortcuts import render
from cliente.models import *

# Create your views here.


def clientes(request):
    clientes=cliente.objects.all()

    return render (request,'clientes/clientes.html',{'clientes':clientes})