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
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/new/', views.create_goal, name='create_goal'),
    path('goals/<int:pk>/edit/', views.update_goal, name='update_goal'),
    path('goals/<int:pk>/delete/', views.delete_goal, name='delete_goal'),
    path('goals/<int:pk>/add-contribution/', views.add_contribution, name='add_contribution'),
    path('goals/<int:pk>/contributions/', views.get_contributions, name='get_contributions'),
    path('goals/ai-insight/', views.ai_goal_insight, name='ai_goal_insight'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/new/', views.create_report, name='create_report'),
    path('signup/', views.signup, name='signup'),
]