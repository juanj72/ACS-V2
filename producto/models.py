from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return str(self.nombre)

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    valor_neto = models.IntegerField()
    valor_publico = models.IntegerField()
    cantidad = models.IntegerField()
    categoria = models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return str(self.id)+'. '+str(self.nombre)+', Precio: $'+str(self.valor_publico)+' Cat >>'+str(self.categoria)+', Cantidad en stock: '+str(self.cantidad)

    class Meta:
        db_table = 'producto'