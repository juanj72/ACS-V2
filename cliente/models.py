from django.db import models

# Create your models here.


class cliente (models.Model):
    documento = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255,null=True)
    class Meta:
        db_table = 'cliente'