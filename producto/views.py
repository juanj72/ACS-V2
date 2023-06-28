from django.shortcuts import render
from producto.models import *

# Create your views here.

def productos (request):
    productos= producto.objects.all()
    return render(request,'productos/productos.html',{'productos':productos})

def categorias(request):
    categorias=categoria.objects.all()
    return render(request,'productos/categorias.html',{'categorias':categorias})