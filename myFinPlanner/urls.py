from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Prefijo para home y accounts
    path('finances/', include('finances.urls')),  # Prefijo para finances
    path('investments/', include('investments.urls')),  # Prefijo para investments
]

# Añadir esta configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)