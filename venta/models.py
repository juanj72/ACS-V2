from django.db import models
from cliente.models import Cliente
from producto.models import producto
from user.models import User
from django.utils.timezone import now
# Create your models here.

class estado (models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id)+'. '+str(self.nombre)

class recibo (models.Model):
    cliente=models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey(estado,on_delete=models.SET_NULL,null=True,default=1)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    fecha = models.DateTimeField(auto_created=True,default=now)


class detalle (models.Model):
    producto=models.ForeignKey(producto,on_delete=models.SET_NULL,null=True)
    cantidad = models.IntegerField()
    recibo = models.ForeignKey(recibo,on_delete=models.SET_NULL,null=True)
    fecha = models.DateTimeField(auto_now=True)

class log_anulados(models.Model):
    motivo = models.TextField()
    recibo = models.ForeignKey(recibo,on_delete=models.SET_NULL,null=True)
