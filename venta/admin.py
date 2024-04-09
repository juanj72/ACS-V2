from django.contrib import admin

from venta.models import Detalle, Estado, LogAnulados, Recibo

# Register your models here.

admin.site.register(Estado)
admin.site.register(Detalle)
admin.site.register(Recibo)
admin.site.register(LogAnulados)
