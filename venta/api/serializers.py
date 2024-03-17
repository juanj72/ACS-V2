from rest_framework import serializers

from venta.models import *
from cliente.api.serializers import ClienteSerializer


class EstadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estado
        fields = '__all__'


class ReciboSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recibo
        fields = '__all__'

