# Generated by Django 3.2.8 on 2021-10-21 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentirsebien', '0006_perfil_dni'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataunfv',
            name='anio_ingreso',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]