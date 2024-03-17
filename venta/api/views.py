from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import F

from venta.models import *
from venta.api.serializers import *
from venta.api.utils import total_detalle


class ReciboCreateView(APIView):

    def post(self, request, cliente_id, *args, **kwargs):
        serializer = ReciboSerializer(
            data={**request.data, 'cliente': cliente_id})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleVentaListView(APIView):

    def get(self, request, recibo_id, *args, **kwargs):
        recibo = Recibo.objects.get(id=recibo_id)
        recibo_serializer = ReciboSerializer(recibo)

        if (recibo.estado.id != 1):
            return Response({'message': 'El estado del recibo es 1'}, status=status.HTTP_404_NOT_FOUND)

        productos = Detalle.objects.filter(recibo=recibo).annotate(
            resultado=F('cantidad') * F('producto__valor_publico'))
        detalle_serializer = DetalleSerializer(productos, many=True)

        total = total_detalle(recibo_id)

        return Response({
            'detalle': recibo_serializer.data,
            'productos': detalle_serializer.data,
            'total': total
        }, status=status.HTTP_200_OK)


class CerrarReciboView(APIView):

    def put(self, request, recibo_id, *args, **kwargs):
        recibo = Recibo.objects.get(id=recibo_id)

        if (recibo.estado.id == 1):
            # Asigna el nuevo valor de estado (por ejemplo, 2)
            nuevo_estado = Estado.objects.get(id=2)
            recibo.estado = nuevo_estado  # Asigna el nuevo estado al recibo

            recibo.save()

            serializer = ReciboSerializer(recibo)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': '404 - PÁGINA NO ENCONTRADA'}, status=status.HTTP_404_NOT_FOUND)
