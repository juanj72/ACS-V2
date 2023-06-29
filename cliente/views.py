from django.shortcuts import render,redirect
from cliente.models import *
from cliente.forms import *
# Create your views here.


def clientes(request):
    clientes=cliente.objects.all()

    return render (request,'clientes/clientes.html',{'clientes':clientes})



def crearCliente(request):

    formulario = formulario_cliente(request.POST or None)

    if request.method == 'POST':
        if formulario.is_valid():
            dato=formulario.save()

            print(dato.id)
            return redirect('crearrecibo',dato.id)
        else:
            formulario.errors

    return render (request,'clientes/crearCliente.html',{'formulario':formulario})