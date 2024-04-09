from django.shortcuts import redirect, render

from cliente.forms import formulario_cliente
from cliente.models import Cliente

# Create your views here.


def clientes(request):
    clientes = Cliente.objects.all()

    return render(request, "clientes/clientes.html", {"clientes": clientes})


def crearCliente(request):
    formulario = formulario_cliente(request.POST or None)

    if request.method == "POST":
        if formulario.is_valid():
            dato = formulario.save()

            print(dato.id)
            return redirect("crearrecibo", dato.id)
        else:
            formulario.errors

    return render(request, "clientes/crearCliente.html", {"formulario": formulario})


def asignarClienteVenta(request):
    clientes = Cliente.objects.all()

    return render(request, "clientes/venta.html", {"clientes": clientes})


def editar(request, id):
    formulario = formulario_cliente(request.POST or None, instance=Cliente.objects.get(id=id))
    if request.method == "POST":
        if formulario.is_valid:
            formulario.save()
            return redirect("clientes")
        else:
            formulario.errors

    return render(request, "clientes/edit.html", {"formulario": formulario})
