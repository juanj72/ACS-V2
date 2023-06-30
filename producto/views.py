from django.shortcuts import render,redirect
from producto.models import *
from producto.forms import *

# Create your views here.

def productos (request):
    productos= producto.objects.all()
    formulario = productoForm(request.POST or None)

    if request.method=='POST':
        if formulario.is_valid:
            formulario.save()
            return redirect('productos')

    return render(request,'productos/productos.html',{'productos':productos,'formulario':formulario})

def categorias(request):
    categorias=categoria.objects.all()
    formulario = categoriaForm(request.POST or None)
    if request.method=='POST':
        if formulario.is_valid:
            formulario.save()
            return redirect('categorias')
    
    return render(request,'productos/categorias.html',{'categorias':categorias,'formulario':formulario})