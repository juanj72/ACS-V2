from django.shortcuts import render,redirect
from venta.models import *
from cliente.models import cliente
from venta.forms import *

# Create your views here.

def venta(request):

    return render(request,'ventas/select.html')


def crearrecibo(request,client):

    reb = recibo(
        cliente = cliente.objects.get(id=client),
        user=request.user
    )
    reb.save()
    print(reb.id)
   

    return redirect ('detalle',reb.id)



def detalleventa(request,reb):
    re = recibo.objects.get(id=reb)
    productos=detalle.objects.filter(recibo = re)
    formulario = detalleVentaForm(request.POST or None,initial={'recibo':re})
    error = False

    if request.method == 'POST':
        if formulario.is_valid:

            data=formulario
            pro = producto.objects.get(id=data.data['producto'])
            if int(data.data['cantidad'])>pro.cantidad:
                print('la cantidad supera el limite en stock')
                error = True
            else:
                pro.cantidad=int(pro.cantidad)-int(data.data['cantidad'])
                pro.save()
                data.save()
            
                return redirect('detalle',reb)

        else:
            formulario.errors()

    return render (request, 'ventas/detalle.html',{'detalle':reb,'formulario':formulario,'productos':productos,'error':error})



def eliminardetail(request,id,reb):
    re = recibo.objects.get(id=reb)
    detail = detalle.objects.get(id=id)
    pro=producto.objects.get(id=detail.producto.id)
    pro.cantidad=int(pro.cantidad)+int(detail.cantidad)
    pro.save()

    detail.delete()

    return redirect('detalle',re.id)