from django import forms
from venta.models import *


class detalleVentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = detalle
        fields = '__all__'
        widgets = {
             'recibo':forms.HiddenInput()
        }


class anularForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

    class Meta:
          model = log_anulados
          fields = '__all__'
          widgets = {
             'recibo':forms.HiddenInput()
        }
