from django.contrib import admin
from .models import Perfil, FichaSociodemografica, ItemsTopicos, ComponenteBienestar, RespuestasPuente, ResultadoPerfil
from import_export import resources
from import_export.admin import ImportExportModelAdmin 

# Register your models here.
admin.site.register(Perfil)
admin.site.register(FichaSociodemografica)
admin.site.register(ResultadoPerfil)
admin.site.register(RespuestasPuente)


class ItemsTopicosResource(resources.ModelResource):
    class Meta:
        model = ItemsTopicos

class ItemsTopicosAdmin(ImportExportModelAdmin,admin.ModelAdmin): # new
    search_fields = ['item']
    list_display = ('topico','item','estado','creado','actualizado',)
    resources_class = ItemsTopicosResource

admin.site.register(ItemsTopicos, ItemsTopicosAdmin)


class ComponenteBienestarResource(resources.ModelResource):
    class Meta:
        model = ComponenteBienestar

class ComponenteBienestarAdmin(ImportExportModelAdmin,admin.ModelAdmin): # new
    search_fields = ['item']
    list_display = ('perfil','topico','completado','estado','creado','actualizado',)
    resources_class = ComponenteBienestarResource

admin.site.register(ComponenteBienestar, ComponenteBienestarAdmin)

