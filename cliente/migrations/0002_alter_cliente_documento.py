# Generated by Django 4.2.2 on 2023-06-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='documento',
            field=models.IntegerField(unique=True),
        ),
    ]
