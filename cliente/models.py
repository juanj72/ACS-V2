from django.db import models

# Create your models here.


class cliente (models.Model):
    documento = models.IntegerField()
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    class Meta:
        db_table = 'cliente'