from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cliente.api.serializers import ClienteSerializer
from cliente.models import Cliente


class ClientesListView(APIView):

    def get(self, request, *args, **kwargs):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ClienteCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteView(APIView):

    def patch(self, request, cliente_id, *args, **kwargs):
        cliente = Cliente.objects.get(id=cliente_id)
        serializer = ClienteSerializer(
            cliente, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
