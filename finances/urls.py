from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/new/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/new/', views.create_budget, name='create_budget'),
    path('budgets/<int:pk>/edit/', views.update_budget, name='update_budget'),
    path('budgets/<int:pk>/delete/', views.delete_budget, name='delete_budget'),
    path('investments/', views.investment_list, name='investment_list'),
    path('investments/add/', views.add_investment, name='add_investment'),
    path('investments/delete/<int:pk>/', views.delete_investment, name='delete_investment'),
    path('investments/update-symbols/', views.update_symbols, name='update_symbols'),
    path('investments/update-price/', views.update_price, name='update_price'),
    path('api/symbols/', views.symbol_search, name='symbol_search'),
    path('api/price/<str:symbol>/', views.get_price, name='get_price'),
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/new/', views.create_goal, name='create_goal'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/new/', views.create_report, name='create_report'),
    path('signup/', views.signup, name='signup'),
]