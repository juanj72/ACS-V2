# Generated by Django 4.2.2 on 2023-06-28 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0002_recibo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='estado',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='venta.estado'),
        ),
    ]
