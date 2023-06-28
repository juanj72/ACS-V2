from django import forms
from cliente.models import *
from dataclasses import fields


class formulario_cliente(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'


    class Meta:
        model = cliente
        fields = '__all__'