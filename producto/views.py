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


def addcantidadpro(request,pro):
    prod=producto.objects.get(id=pro)
   
    if request.method=='POST':
        prod.cantidad = int(prod.cantidad)+int(request.POST.get('cantidad'))
        prod.save()
        return redirect('productos')

       
    return render (request,'productos/addcantidad.html',{'producto':prod})

def editar_producto(request,id):
    formulario = productoForm(request.POST or None,instance=producto.objects.get(id=id))

    if request.method=='POST':
      
        if formulario.is_valid():
            formulario.save()
            return redirect('productos')
    return render (request,'productos/editar.html',{'formulario':formulario})

def editar_categoría(request,id):
    formulario = categoriaForm(request.POST or None,instance=categoria.objects.get(id=id))
    if request.method=='POST':
        if formulario.is_valid():
            formulario.save()
            return redirect('categorias')
    return render(request,'productos/editcat.html',{'formulario':formulario})




