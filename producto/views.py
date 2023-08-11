from django.shortcuts import render,redirect
from producto.models import *
from producto.forms import *
from django.db import connection

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


def reportes(request):
    productos_mas = productos_mas_vendidos()
  
    return render(request,'reportes/general.html',{'productos':productos_mas})

def detalle_reporte(request):
    return render(request,'reportes/detallados.html')


def productos_mas_vendidos():
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    
        sql = f"""
    SELECT 
   p.id, p.nombre, SUM(v.cantidad) AS 'cantidad_vendida',
   p.valor_publico,
   SUM(v.cantidad)*p.valor_publico as valor_vendido_publico
FROM
    venta_detalle v
        INNER JOIN
    producto p ON p.id = v.producto_id
GROUP BY p.id
ORDER BY  SUM(v.cantidad)*p.valor_publico DESC
LIMIT 5

        """

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(sql)
        #total=total_fecha(fecha)

        columns = []  # Para guardar el nombre de las columnas

        # Recorrer la descripcion (Nombre de la columna)
        for column in cursor.description:

            columns.append(column[0])  # Guardando el nombre de las columnas

        data = []  # Lista con los datos que vamos a enviar en JSON

        for row in cursor.fetchall():  # Recorremos las fila guardados de la BD

            # Insertamos en data un diccionario
            data.append(dict(zip(columns, row)))

        cursor.close()  # Se cierra el cursor para que se ejecute el procedimiento almacenado

        connection.commit()  # Enviamos la sentencia a la BD
        connection.close()

        return(data)



