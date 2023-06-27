from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import *

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets=(
        (None,{
        'fields':('username','password')
        }),

        ('Información personal',{
        'fields':('first_name','last_name','email',)
        }),
        ('Permisos',{
        'fields':(
        'is_superuser',
        'is_staff',
        'is_active'
        ),
        }),
        ('Rol',{
        'fields':(
        'rol',
        ),
        }),
    )

admin.site.register(Rol)