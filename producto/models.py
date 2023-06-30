from django.db import models

# Create your models here.

class categoria(models.Model):
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return str(self.nombre)

class producto(models.Model):
    nombre = models.CharField(max_length=255)
    valor_neto = models.IntegerField()
    valor_publico = models.IntegerField()
    cantidad = models.IntegerField()
    categoria = models.ForeignKey(categoria,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return str(self.id)+'. '+str(self.nombre)+' Cat >>'+str(self.categoria)

    class Meta:
        db_table = 'producto'