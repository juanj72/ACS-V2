from django.shortcuts import render,redirect
from venta.models import recibo,estado
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import connection

# Create your views here.
@login_required
def index(request):
    recibos = recibo.objects.filter(estado=estado.objects.get(id=1))
    print(len(recibos))
    return render(request,'index.html',{'recibos':recibos,'cantidad':len(recibos),'valor_inventario':total_inventario(),'total_stock':total_stock(),'total_vendido':total_vendido()})

@login_required
def confirmacionventa(request,id):

    return render(request,'confirmaciones/ventaok.html',{'id':id})

@login_required
def cerrar_sesion(request):

    logout(request)

    return redirect('/')



def total_inventario():
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    
        sql = """
      select sum(valor_neto*cantidad) as total from producto;
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
     

def total_stock():
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    
        sql = """
     select count(id) cantidad from producto
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
     
     
def total_vendido():
     with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
    
        sql = """
         select sum(sub.total) as total from (
     SELECT 
    re.id as numero_recibo,
    
    est.nombre as estado,
    re.fecha as fecha_recibo,
    concat(c.nombre,' ',c.apellido) as cliente,
    c.documento as documento,
  
    sum(det.cantidad*pro.valor_publico) as 'total'
    
FROM
    venta_recibo re
        INNER JOIN
    cliente c ON c.id = re.cliente_id
        INNER JOIN
    venta_detalle det ON det.recibo_id = re.id
        INNER JOIN
    venta_estado est ON est.id = re.estado_id
    inner join producto pro on det.producto_id=pro.id and re.estado_id = 2
    
    group by re.id
    
    ) as sub
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