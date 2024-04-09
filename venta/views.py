from django.db import connection
from django.db.models import F
from django.shortcuts import HttpResponse, redirect, render

from cliente.models import Cliente
from producto.models import Producto
from venta.forms import anularForm, detalleVentaForm
from venta.models import Detalle, Estado, Recibo

# Create your views here.


def venta(request):
    return render(request, "ventas/select.html")


def crearrecibo(request, client):
    reb = Recibo(cliente=Cliente.objects.get(id=client), user=request.user)
    reb.save()
    print(reb.id)

    return redirect("detalle", reb.id)


def detalleventa(request, reb):
    re = Recibo.objects.get(id=reb)
    if re.estado.id != 1:
        return HttpResponse("404")

    else:
        productos = Detalle.objects.filter(recibo=re).annotate(
            resultado=F("cantidad") * F("producto__valor_publico")
        )
        formulario = detalleVentaForm(request.POST or None, initial={"recibo": re})
        detalle_total = total_detalle(reb)
        error = False
        validador = False
        print(len(productos))
        if len(productos) > 0:
            validador = True
        else:
            validador = False
        print(validador)
        if request.method == "POST":
            try:
                if formulario.is_valid:
                    data = formulario
                    pro = Producto.objects.get(id=data.data["producto"])
                    if int(data.data["cantidad"]) > pro.cantidad:
                        print("la cantidad supera el limite en stock")
                        error = True
                    else:
                        pro.cantidad = int(pro.cantidad) - int(data.data["cantidad"])
                        pro.save()
                        data.save()

                        return redirect("detalle", reb)

                else:
                    formulario.errors
            except Exception:
                formulario.errors

        return render(
            request,
            "ventas/detalle.html",
            {
                "detalle": reb,
                "formulario": formulario,
                "productos": productos,
                "error": error,
                "total": detalle_total,
                "cerrar": validador,
            },
        )


def eliminardetail(request, id, reb):
    re = Recibo.objects.get(id=reb)
    detail = Detalle.objects.get(id=id)
    pro = Producto.objects.get(id=detail.producto.id)
    pro.cantidad = int(pro.cantidad) + int(detail.cantidad)
    pro.save()

    detail.delete()

    return redirect("detalle", re.id)


def total_detalle(recibo):
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
        sql = f"""
                SELECT
    pro.nombre,
    pro.valor_publico,
    SUM(det.cantidad) AS cantidad,
    det.recibo_id,
     coalesce(SUM(pro.valor_publico * det.cantidad) ,0) AS total
FROM
    producto pro
        INNER JOIN
    venta_detalle det ON det.producto_id = pro.id
WHERE
    det.recibo_id = {recibo}
        """

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(sql)
        # total=total_fecha(fecha)

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

        return data


def cerrarrecibo(request, id):
    recibos = Recibo.objects.get(id=id)
    if recibos.estado.id == 1:
        recibos.estado = Estado.objects.get(id=2)
        recibos.save()
        return redirect("okventa", id)
    else:
        return HttpResponse("404, PÁGINA NO ENCONTRADA")


def anular(request, id):
    detalles = Detalle.objects.filter(recibo=id)
    reb = Recibo.objects.get(id=id)
    if reb.estado.id == 3:
        return HttpResponse("404 :( , PAGINA NO ENCONTRADA")
    estados = Estado.objects.get(id=3)
    formulario = anularForm(request.POST or None, initial={"recibo": reb})
    print(len(detalles))

    if request.method == "POST":
        if formulario.is_valid:
            if len(detalles) > 0:
                for det in detalles:
                    productos = Producto.objects.get(id=det.producto.id)
                    productos.cantidad = int(productos.cantidad) + int(det.cantidad)
                    productos.save()
                reb.estado = estados
                reb.save()
                formulario.save()
                return redirect("seleccion")
            else:
                reb.estado = estados
                reb.save()
                formulario.save()
                return redirect("seleccion")
        else:
            formulario.errors

    return render(request, "ventas/anular.html", {"formulario": formulario})


def detalle_recibo(request, id):
    recibos = Recibo.objects.get(id=id)
    detalles = Detalle.objects.filter(recibo=recibos).annotate(
        resultado=F("cantidad") * F("producto__valor_publico")
    )
    total = total_detalle(id)

    return render(
        request,
        "ventas/recibo.html",
        {"detalle": detalles, "recibo": recibos, "total": total},
    )


def listar(request):
    recibos = recibos_lista()
    totall = total()
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("fecha_inicio") and request.POST.get("fecha_fin"):
            recibos = consulta_fechas(
                request.POST.get("fecha_inicio"), request.POST.get("fecha_fin")
            )
            totall = total_fecha(
                request.POST.get("fecha_inicio"), request.POST.get("fecha_fin")
            )

    return render(
        request, "ventas/verventas.html", {"recibos": recibos, "total": totall}
    )


def recibos_lista():
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
        sql = """
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
        """

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(sql)
        # total=total_fecha(fecha)

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

        return data


def consulta_fechas(fecha_inicio, fecha_fin):
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
        sql = f"""
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
    inner join producto pro on det.producto_id=pro.id

    where date(re.fecha) between date('{fecha_inicio}') and date('{fecha_fin}') and re.estado_id = 2

    group by re.id
        """

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(sql)
        # total=total_fecha(fecha)

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

        return data


def total():
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
        sql = """
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
    inner join producto pro on det.producto_id=pro.id

    where re.estado_id = 2



        """

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(sql)
        # total=total_fecha(fecha)

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

        return data


def total_fecha(fecha_inicio, fecha_fin):
    with connection.cursor() as cursor:  # Activamos un cursor para las consultas a la BD
        sql = f"""
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
    inner join producto pro on det.producto_id=pro.id

    where date(re.fecha) between date('{fecha_inicio}') and date('{fecha_fin}') and re.estado_id = 2

        """

        # Ejecutar una linea SQL En este caso llamamos un procedimiento almacenado
        cursor.execute(sql)
        # total=total_fecha(fecha)

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

        return data
