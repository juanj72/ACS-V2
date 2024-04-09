from rest_framework import serializers

from producto.models import Categoria, Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"


class ProductoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["cantidad"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class ReporteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    cantidad_vendida = serializers.IntegerField()
    valor_publico = serializers.DecimalField(max_digits=10, decimal_places=2)
    valor_vendido_publico = serializers.DecimalField(max_digits=10, decimal_places=2)
