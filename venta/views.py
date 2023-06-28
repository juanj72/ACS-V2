from django.shortcuts import render

# Create your views here.

def venta(request):
    return render(request,'ventas/select.html')