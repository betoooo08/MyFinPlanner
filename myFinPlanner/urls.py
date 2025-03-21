from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finances.urls')),  # Prefijo para finances
    path('investments/', include('investments.urls')),  # Prefijo para investments
    path('accounts/', include('django.contrib.auth.urls')),  # Prefijo para autenticación
]