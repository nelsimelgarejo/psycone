from django.urls import path
from psycone import settings
from django.conf.urls.static import static
from .views import usuarios, dashboard

urlpatterns = [
    #Login y registro
    path('', usuarios.ingreso_sistema, name='ingreso_sistema'),
    path('activar/cuenta', usuarios.activar_cuenta, name='activar_cuenta'),
    path('activacion/<str:encoded_url>/cuenta', usuarios.aprobar_encode, name='aprobar_encode'),
    path('change/password', usuarios.cambiar_contrasenia, name='cambiar_contrasenia'),
    path('ingreso/bienvenida', usuarios.previo_ingreso, name='previo_ingreso'),
    path('ingreso/universidades', usuarios.post_ingreso_universidades, name='post_ingreso_universidades'),
    path('ingreso/otros', usuarios.post_ingreso_otros, name='post_ingreso_otros'),

    #Bashboard
    path('home', dashboard.home, name='home'),
]
if settings.IN_DEVELOPMENT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

