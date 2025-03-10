from django.urls import path
from . import views

urlpatterns = [
    path("", views.transactions_list, name="transaction_list"),
    path("add/", views.create_transaction, name="add_transaction"),
    path('<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('budget/new/', views.create_budget, name='create_budget'),
]