from django.contrib import admin
from django.urls import path, include
from transactions import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("transactions/", include("transactions.urls")),

]
