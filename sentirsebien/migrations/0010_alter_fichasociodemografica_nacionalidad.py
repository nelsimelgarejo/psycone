# Generated by Django 3.2.8 on 2021-10-22 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentirsebien', '0009_alter_fichasociodemografica_anio_estudio_actual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichasociodemografica',
            name='nacionalidad',
            field=models.CharField(blank=True, choices=[('peru', 'Perú'), ('chile', 'Chile'), ('paraguay', 'Paraguay'), ('colombia', 'Colombia'), ('venezuela', 'Venezuela'), ('otros', 'Otros')], default='peru', max_length=30, null=True),
        ),
    ]
