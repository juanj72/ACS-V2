from django.db import connection


def total_detalle(recibo_id):
    """
    Obtiene el total de ventas detalladas para un recibo específico.

    Args:
        recibo_id (int): El ID del recibo para el cual se desea obtener el total de ventas detalladas.

    Returns:
        list: Una lista de diccionarios que representan los detalles de venta para el recibo dado.
            Cada diccionario contiene información sobre el nombre del producto, su valor público,
            la cantidad vendida, el ID del recibo y el total calculado.

    Raises:
        None
    """

    # Establecer conexión con la base de datos y abrir un cursor para ejecutar consultas SQL
    with connection.cursor() as cursor:
        # Construir la consulta SQL para obtener los detalles de venta

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
                    det.recibo_id = {recibo_id}
                """

        # Ejecutar la consulta SQL
        cursor.execute(sql)

        # Obtener los nombres de las columnas del resultado de la consulta
        columns = [column[0] for column in cursor.description]

        # Construir una lista de diccionarios a partir de los resultados de la consulta
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return data
