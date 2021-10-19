# Generated by Django 3.2.8 on 2021-10-19 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sentirsebien', '0003_itemstopicos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemstopicos',
            old_name='usuario',
            new_name='perfil',
        ),
        migrations.AlterField(
            model_name='itemstopicos',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='ComponenteBienestar',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('topico', models.CharField(choices=[('sa_mental', 'SALUD MENTAL POSITIVA'), ('asertividad', 'ASERTIVIDAD'), ('ae_pepresion', 'ANSIEDAD, ESTRÉS Y DEPRESIÓN'), ('ap_social', 'APOYO SOCIAL'), ('vi_pareja', 'VIOLENCIA DE PAREJA')], max_length=20)),
                ('completado', models.BooleanField(default=False)),
                ('estado', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sentirsebien.perfil')),
            ],
        ),
    ]
