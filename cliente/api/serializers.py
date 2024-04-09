from rest_framework import serializers

from cliente.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"

    def validate_documento(self, value):
        """
        Validar que el documento sean números
        """
        if not value.isdigit():
            raise serializers.ValidationError("Asegúrese de ingresar solo números")

        return value
