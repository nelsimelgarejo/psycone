from django.urls import path
from .views import index
from psycone import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
]
if settings.IN_DEVELOPMENT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

