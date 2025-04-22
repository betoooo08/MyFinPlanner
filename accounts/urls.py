from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Ruta para la página principal
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]