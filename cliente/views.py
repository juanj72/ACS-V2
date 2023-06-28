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
        dato=formulario.save()

        print(dato.id)
        return redirect('crearrecibo',dato.id)

    return render (request,'clientes/crearCliente.html',{'formulario':formulario})