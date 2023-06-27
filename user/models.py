from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Rol(models.Model):
    nombre = models.CharField(max_length=255)

class User (AbstractUser):
    rol = models.ForeignKey(Rol,on_delete=models.SET_NULL,null=True,blank=True)
    email = models.EmailField()
    class Meta:
        db_table = 'user'

