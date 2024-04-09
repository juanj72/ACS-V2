from django import forms

from venta.models import Detalle, LogAnulados


class detalleVentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    cantidad = forms.ChoiceField(choices=[(x, x) for x in range(1, 51)])

    class Meta:
        model = Detalle
        fields = "__all__"
        widgets = {"recibo": forms.HiddenInput()}


class anularForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = LogAnulados
        fields = "__all__"
        widgets = {"recibo": forms.HiddenInput()}
