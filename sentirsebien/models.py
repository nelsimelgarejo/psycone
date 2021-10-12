from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

TIPOS_USUARIOS = (
    ('admin', 'Admin'),
    ('estudiante', 'Estudiante'),
    ('docente', 'Docente'),
    ('administrativo', 'Personal administrativo')
)

TIPOS_UNVIERSIDADES = (
    ('unfv', 'Universidad Nacional Federico Villareal'),
    ('red_acacia', 'Red Acacia'),
)

class Perfil(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_universitario = models.CharField(max_length=20, blank=True, null=True)
    universidad = models.CharField(choices=TIPOS_UNVIERSIDADES, max_length=20, blank=True, null=True)
    tipo_usuario = models.CharField(choices=TIPOS_USUARIOS, max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    facebook = models.URLField( blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkeding = models.URLField(blank=True, null=True)

    estado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        self.codigo_universitario = self.usuario.username
        return super(Perfil, self).save(*args, **kwargs)


class FichaSociodemografica(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    anio_ingreso = models.PositiveIntegerField(default=0)
    anio_estudio_actual = models.CharField(max_length=10, blank=True, null=True)
    is_becario = models.BooleanField(default=False)
    facultad = models.CharField(max_length=30, blank=True, null=True)
    escuela = models.CharField(max_length=30, blank=True, null=True)
    sexo = models.CharField(max_length=30, blank=True, null=True)
    genero = models.CharField(max_length=30, blank=True, null=True)
    estado_civil = models.CharField(max_length=30, blank=True, null=True)
    nacimiento_departamento = models.CharField(max_length=30, blank=True, null=True)
    nacimiento_provincia = models.CharField(max_length=30, blank=True, null=True)
    nacimiento_distrito = models.CharField(max_length=30, blank=True, null=True)
    residencia_departamento = models.CharField(max_length=30, blank=True, null=True)
    residencia_provincia = models.CharField(max_length=30, blank=True, null=True)
    residencia_distrito = models.CharField(max_length=30, blank=True, null=True)
    tipo_colegio = models.CharField(max_length=30, blank=True, null=True)
    nacionalidad = models.CharField(max_length=30, blank=True, null=True)
    tiempo_lugar_residencia = models.PositiveIntegerField(default=0)
    religion = models.CharField(max_length=30, blank=True, null=True)
    nivel_socioeconomico = models.CharField(max_length=30, blank=True, null=True)
    vives_solo = models.BooleanField(default=False) 
    vive_con = models.CharField(max_length=100, blank=True, null=True)
    con_cuantos_vives = models.PositiveIntegerField(default=0)
    situacion_ocupacional = models.CharField(max_length=100, blank=True, null=True)
    situacion_de_trabajo = models.CharField(max_length=100, blank=True, null=True)
    horas_apoyo_voluntariado = models.PositiveIntegerField(default=0)
    problema_fisico = models.CharField(max_length=255, blank=True, null=True)
    problema_psicologico = models.CharField(max_length=255, blank=True, null=True)
    tuvo_atencion_psicologica = models.BooleanField(default=False) 
    sintomas_covid_19 = models.BooleanField(default=False) 
    familiar_sintomas_covid_19 = models.BooleanField(default=False) 
    tuvo_fallecimiento = models.CharField(max_length=30, blank=True, null=True) 
    tiempo_de_fallecimiento = models.PositiveIntegerField(default=0)
    adaptado_clases_virtuales = models.BooleanField(default=False) 


    estado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.perfil.codigo_universitario}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()

        return super(FichaSociodemografica, self).save(*args, **kwargs)