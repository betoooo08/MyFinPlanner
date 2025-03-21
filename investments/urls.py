from django.urls import path
from . import views

urlpatterns = [
    path('', views.investment_list, name='investment_list'),
    path('add/', views.add_investment, name='add_investment'),
    path('delete/<int:pk>/', views.delete_investment, name='delete_investment'),
    path('update-symbols/', views.update_symbols, name='update_symbols'),
    path('update-price/', views.update_price, name='update_price'),
    path('api/symbols/', views.symbol_search, name='symbol_search'),  # Ruta para buscar símbolos
    path('api/price/<str:symbol>/', views.get_price, name='get_price'),  # Ruta para obtener precio
]