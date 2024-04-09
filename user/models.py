from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Rol(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id) + ". " + str(self.nombre)


class User(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()

    class Meta:
        db_table = "user"
