from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from producto.api.serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    ProductoStockSerializer,
    ReporteSerializer,
)
from producto.models import Categoria, Producto


class ProductoListView(APIView):
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()

        serializer = ProductoSerializer(productos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductoCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoAddCantidadView(APIView):
    def put(self, request, producto_id, *args, **kwargs):
        producto = Producto.objects.get(id=producto_id)

        try:
            cantidad_a_agregar = int(request.data.get("cantidad", 0))
        except ValueError:
            return Response(
                {"error": "La cantidad debe ser un número entero"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductoStockSerializer(producto, data={"cantidad": producto.cantidad + cantidad_a_agregar})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoView(APIView):
    def put(self, request, producto_id, *args, **kwargs):
        producto = Producto.objects.get(id=producto_id)

        serializer = ProductoSerializer(producto, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaListView(APIView):
    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()

        serializer = CategoriaSerializer(categorias, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriaCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CategoriaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaView(APIView):
    def put(self, request, categoria_id, *args, **kwargs):
        categoria = Categoria.objects.get(id=categoria_id)

        serializer = CategoriaSerializer(categoria, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportesView(APIView):
    def get(self, request):
        productos_mas_vendidos = self.productos_mas_vendidos()

        serializer = ReporteSerializer(productos_mas_vendidos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def productos_mas_vendidos(self):
        with connection.cursor() as cursor:
            sql = """
                SELECT
                    p.id, p.nombre, SUM(v.cantidad) AS cantidad_vendida,
                    p.valor_publico,
                    SUM(v.cantidad) * p.valor_publico as valor_vendido_publico
                FROM
                    venta_detalle v
                        INNER JOIN
                    producto p ON p.id = v.producto_id
                GROUP BY p.id
            """

            cursor.execute(sql)
            columns = [column[0] for column in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            cursor.close()

            connection.commit()
            connection.close()

            return data
