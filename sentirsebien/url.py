from django.urls import path
from psycone import settings
from django.conf.urls.static import static
from .views import usuarios, dashboard, processing

urlpatterns = [
    #Login y registro
    path('', usuarios.ingreso_sistema, name='ingreso_sistema'),
    path('salir/sistema', usuarios.salir_cuenta, name='salir_cuenta'),
    path('activar/cuenta', usuarios.activar_cuenta, name='activar_cuenta'),
    path('activacion/<str:encoded_url>/cuenta', usuarios.aprobar_encode, name='aprobar_encode'),
    path('change/<str:encoded_url>/password', usuarios.cambiar_contrasenia_encode, name='cambiar_contrasenia_encode'),
    path('cambiar/contrasenia', usuarios.cambiar_contrasenia, name='cambiar_contrasenia'),
    path('ingreso/bienvenida', usuarios.previo_ingreso, name='previo_ingreso'),
    path('ingreso/universidades', usuarios.post_ingreso_universidades, name='post_ingreso_universidades'),
    path('ingreso/otros', usuarios.post_ingreso_otros, name='post_ingreso_otros'),
    path('codigo/universitario/validacion', usuarios.codigo_universitario, name='codigo_universitario'),
    path('dni/usuario/validacion', usuarios.dni_usuario, name='dni_usuario'),
    
    #Dashboard
    path('home', dashboard.home, name='home'),
    path('ficha/sociodemografica', dashboard.ficha_sociodemografica, name='ficha_sociodemografica'),
    path('perfil', dashboard.ver_perfil, name='ver_perfil'),
    path('resultados', dashboard.ver_resultados, name='ver_resultados'),
    path('send/resultados/json', dashboard.get_resultados_json, name='get_resultados_json'),

    #Processing
    path('primer/item', processing.primer_item, name='primer_item'),
    path('respuesta/sa_mental', processing.respuesta_sa_mental, name='respuesta_sa_mental'),

]
if settings.IN_DEVELOPMENT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

