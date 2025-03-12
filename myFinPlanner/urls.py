from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from finances import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.dashboard, name='transactions'),  # Placeholder
    path('budgets/', views.dashboard, name='budgets'),  # Placeholder
    path('investments/', views.dashboard, name='investments'),  # Placeholder
    path('goals/', views.dashboard, name='goals'),  # Placeholder
    path('reports/', views.dashboard, name='reports'),  # Placeholder
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)