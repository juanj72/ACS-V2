from django.shortcuts import render
from venta.models import recibo,estado


# Create your views here.

def index(request):
    recibos = recibo.objects.filter(estado=estado.objects.get(id=1))
    print(len(recibos))
    return render(request,'index.html',{'recibos':recibos,'cantidad':len(recibos)})

def confirmacionventa(request,id):

    return render(request,'confirmaciones/ventaok.html',{'id':id})


