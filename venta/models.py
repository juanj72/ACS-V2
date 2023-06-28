from django.db import models
from cliente.models import cliente
from producto.models import producto
from user.models import User

# Create your models here.

class estado (models.Model):
    nombre = models.CharField(max_length=255)

class recibo (models.Model):
    cliente=models.ForeignKey(cliente, on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey(estado,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    
    
class detalle (models.Model):
    producto=models.ForeignKey(producto,on_delete=models.SET_NULL,null=True)
    cantidad = models.IntegerField()
    recibo = models.ForeignKey(recibo,on_delete=models.SET_NULL,null=True)
    fecha = models.DateTimeField(auto_now=True)


    