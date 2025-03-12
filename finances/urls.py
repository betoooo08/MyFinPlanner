from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Transactions
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/new/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    
    # Budgets
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/new/', views.create_budget, name='create_budget'),
    path('budgets/<int:pk>/edit/', views.update_budget, name='update_budget'),
    path('budgets/<int:pk>/delete/', views.delete_budget, name='delete_budget'),
]