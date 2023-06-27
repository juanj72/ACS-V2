from django.db import models

# Create your models here.

class categoria(models.Model):
    nombre = models.CharField(max_length=255)

class producto(models.Model):
    nombre = models.CharField(max_length=255)
    valor_neto = models.IntegerField()
    valor_publico = models.IntegerField()
    cantidad = models.IntegerField()
    categoria = models.ForeignKey(categoria,on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = 'producto'