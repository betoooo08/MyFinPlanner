from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),  # Ruta para la página principal
    path('signup/', views.signup_view, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]